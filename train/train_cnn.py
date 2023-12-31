import argparse
import os
import random
from datetime import datetime
from glob import glob

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms
import yaml
from mlflow import log_metric, log_param, log_params, set_experiment, start_run
from PIL import Image, ImageFile
from torch.autograd import Variable
from torch.utils.data import DataLoader
from tqdm import tqdm


class CNNTrainer:
    def __init__(self, CONFIG_PATH) -> None:
        self.CONFIG_PATH = CONFIG_PATH
        self.config = self.load_settings()
        assert self.config["CNN"]["classification"] == len(
            self.config["TARGETS"]
        ), "In setting.yaml classification and WEIGHTS must be length."
        assert (
            self.config["PREPARE"]["batch_size"] > 0 and self.config["CNN"]["epoch"] > 0
        ), "In setting.yaml batch_size and epochs types must be integer."
        self.EPOCHS = self.config["CNN"]["epoch"]
        SEED = self.config["CNN"]["seed"]
        random.seed(SEED)
        np.random.seed(SEED)
        torch.manual_seed(SEED)
        torch.cuda.manual_seed(SEED)
        torch.backends.cudnn.deterministic = True
        work_dir = self.config["PATH"]["work"]
        self.data_dir = self.config["PATH"]["data"]
        date = datetime.now()
        self.save_dir = f"{work_dir}{date.strftime('%Y%m%d%H%M')}_{self.config['EXPERIMENTS']['ver']}"
        os.makedirs(self.save_dir, exist_ok=True)
        self.save_dir = f"{self.save_dir}/"
        SAVE_DIR = self.config["PATH"]["model"]
        CNN_FILE = f"{self.config['CNN']['backborn']}-{self.config['CNN']['mode']}-{self.config['CNN']['classification']}cls.pt"
        self.MODEL_SAVE_PATH = f"{self.save_dir}{CNN_FILE}"
        self.MODEL_SAVE_PATH2 = os.path.join(SAVE_DIR, CNN_FILE)
        os.makedirs(SAVE_DIR, exist_ok=True)
        self.device = torch.device("cuda")

    def load_settings(self):
        with open(self.CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)

    def prepare_transform(self):
        train_transforms = transforms.Compose(
            [
                transforms.RandomHorizontalFlip(),
                transforms.RandomGrayscale(p=0.2),
                transforms.RandomChoice(
                    [
                        transforms.ColorJitter(
                            brightness=0.5, contrast=0.2, saturation=0.2
                        ),
                        transforms.RandomRotation(10),
                        transforms.RandomRotation(30),
                    ]
                ),
                transforms.RandomChoice(
                    [
                        transforms.Resize((448, 448)),
                        transforms.Resize((416, 416)),
                        transforms.Resize((400, 400)),
                    ]
                ),
                transforms.RandomCrop((384, 384)),
                transforms.Resize((384, 384)),
                transforms.ToTensor(),
            ]
        )
        test_transforms = transforms.Compose(
            [
                transforms.Resize((384, 384)),
                transforms.ToTensor(),
            ]
        )

        return train_transforms, test_transforms

    def load_data(self):
        train_transforms, test_transforms = self.prepare_transform()
        train_data = datasets.ImageFolder(f"{self.data_dir}/train", train_transforms)
        valid_data = datasets.ImageFolder(f"{self.data_dir}/test", test_transforms)
        test_data = datasets.ImageFolder(f"{self.data_dir}/test", test_transforms)
        print(f"Number of training data: {len(train_data)}")
        print(f"Number of validation data: {len(valid_data)}")
        print(f"Number of testing data: {len(test_data)}")

        return train_data, valid_data, test_data

    def shuffle_data(self, train_data, valid_data, test_data):
        BATCH_SIZE = self.config["PREPARE"]["batch_size"]
        train_iterator = DataLoader(
            train_data,
            shuffle=True,
            batch_size=BATCH_SIZE,
            num_workers=os.cpu_count(),
            pin_memory=True,
        )
        valid_iterator = DataLoader(
            valid_data,
            shuffle=True,
            batch_size=BATCH_SIZE,
            num_workers=os.cpu_count(),
            pin_memory=True,
        )
        test_iterator = DataLoader(
            test_data,
            shuffle=True,
            batch_size=BATCH_SIZE,
            num_workers=os.cpu_count(),
            pin_memory=True,
        )
        ImageFile.LOAD_TRUNCATED_IMAGES = True

        return train_iterator, valid_iterator, test_iterator

    def build_model(self):
        if self.config["CNN"]["backborn"] == "efficientnet":
            model = models.efficientnet_v2_s(pretrained=True).to(
                self.device, non_blocking=True
            )
            for param in model.parameters():
                param.requires_grad = True
            model.classifier = nn.Linear(
                in_features=1280, out_features=self.config["CNN"]["classification"]
            ).to(self.device, non_blocking=True)
        elif self.config["CNN"]["backborn"] == "resnet":
            model = models.resnet101(pretrained=True).to(self.device, non_blocking=True)
            for param in model.parameters():
                param.requires_grad = True
            model.fc = nn.Linear(
                in_features=512, out_features=self.config["CNN"]["classification"]
            ).to(self.device, non_blocking=True)
        elif self.config["CNN"]["backborn"] == "mobilenet":
            model = models.mobilenet_v3_small(pretrained=True).to(
                self.device, non_blocking=True
            )
            for param in model.parameters():
                param.requires_grad = True
            model.classifier[3] = nn.Linear(
                in_features=1024, out_features=self.config["CNN"]["classification"]
            ).to(self.device, non_blocking=True)

        return model

    def calculate_accuracy(self, fx, y):
        preds = fx.max(1, keepdim=True)[1]
        correct = preds.eq(y.view_as(preds)).sum()
        acc = correct.float() / preds.shape[0]

        return acc

    def train(self, model, device, iterator, optimizer, criterion):
        epoch_loss, epoch_acc = 0, 0
        model.train()
        scaler = torch.cuda.amp.GradScaler()
        torch.backends.cudnn.benchmark = True

        for x, y in tqdm(iterator):
            x = x.to(device, non_blocking=True)
            y = y.to(device, non_blocking=True)
            optimizer.zero_grad()
            with torch.cuda.amp.autocast():
                fx = model(x)
                loss = criterion(fx, y)
                acc = self.calculate_accuracy(fx, y)
                scaler.scale(loss).backward()
                scaler.step(optimizer)
                scaler.update()
                epoch_loss += loss.item()
                epoch_acc += acc.item()

        return epoch_loss / len(iterator), epoch_acc / len(iterator)

    def evaluate(self, model, device, iterator, criterion):
        epoch_loss, epoch_acc = 0, 0
        model.eval()

        with torch.no_grad():
            for x, y in iterator:
                x = x.to(device, non_blocking=True)
                y = y.to(device, non_blocking=True)
                fx = model(x)
                loss = criterion(fx, y)
                acc = self.calculate_accuracy(fx, y)
                epoch_loss += loss.item()
                epoch_acc += acc.item()

        return epoch_loss / len(iterator), epoch_acc / len(iterator)

    def predict_image(self, image, transforms, model):
        image_tensor = transforms(image).float()
        image_tensor = image_tensor.unsqueeze_(0)
        # アルファチャンネルを削除する
        image_tensor = image_tensor[:, :3, :, :]

        input = Variable(image_tensor)
        input = input.to(self.device, non_blocking=True)
        output = model(input)
        index = output.data.cpu().numpy().argmax()

        return index

    def predict_dir(self, file_list, transforms, model):
        results = [0] * self.config["CNN"]["classification"]
        for file in file_list:
            img = Image.open(file).convert("RGBA")
            idx = self.predict_image(img, transforms, model)
            results[idx] += 1

        return results

    def adjust_weights(self, model):
        optimizer = optim.Adam(model.parameters())
        train_dirs = sorted(glob(f"{self.config['PATH']['data']}/train/*"))
        test_dirs = sorted(glob(f"{self.config['PATH']['data']}/test/*"))
        train_files, test_files = [], []

        for train_dir, test_dir in zip(train_dirs, test_dirs):
            train_files.append(len(glob(f"{train_dir}/*")))
            test_files.append(len(glob(f"{test_dir}/*")))
            max_file = max(train_files)
            cls_weights = []
            for train_file in train_files:
                cls_weights.append(round(max_file / train_file, 1))
        weights = torch.tensor(cls_weights).cuda()

        for target, train_file, test_file, cls_weight in zip(
            self.config["TARGETS"], train_files, test_files, cls_weights
        ):
            print(f"Class: {target}")
            print(f"Train: {train_file} | Test: {test_file} | Weight: {cls_weight}")
        criterion = nn.CrossEntropyLoss(weight=weights)
        best_valid_loss = float("inf")

        return optimizer, criterion, best_valid_loss, cls_weights

    def log_params(self, cls_weights):
        log_params(
            {
                "batch_size": self.config["PREPARE"]["batch_size"],
                "mode": self.config["CNN"]["mode"],
                "seed": self.config["CNN"]["seed"],
                "backborn": self.config["CNN"]["backborn"],
                "epoch": self.config["CNN"]["epoch"],
                "classification": self.config["CNN"]["classification"],
                "train_data": f"{self.data_dir}/train",
                "valid_data": f"{self.data_dir}/test",
                "test_data": f"{self.data_dir}/test",
            }
        )
        for i in range(self.config["CNN"]["classification"]):
            log_param(f"{i}{self.config['TARGETS'][i]}", cls_weights[i])

    def train_cnn(self, optimizer, criterion, best_valid_loss):
        for epoch in range(self.EPOCHS):
            train_loss, train_acc = self.train(
                model, self.device, train_iterator, optimizer, criterion
            )
            valid_loss, valid_acc = self.evaluate(
                model, self.device, valid_iterator, criterion
            )

            if valid_loss < best_valid_loss:
                best_valid_loss = valid_loss
                torch.save(model.state_dict(), self.MODEL_SAVE_PATH)
            torch.save(model.state_dict(), self.MODEL_SAVE_PATH2)
            print(
                f"| Epoch: {epoch+1:02} | Train Loss: {train_loss:.3f} | Train Acc: {train_acc*100:.2f}% | Val. Loss: {valid_loss:.3f} | Val. Acc: {valid_acc*100:.2f}% |"  # noqa
            )

            log_metric("Train Loss", f"{train_loss:.3f}", epoch + 1)
            log_metric("Train Acc", f"{train_acc*100:.2f}", epoch + 1)
            log_metric("Val. Loss", f"{valid_loss:.3f}", epoch + 1)
            log_metric("Val. Acc", f"{valid_acc*100:.2f}", epoch + 1)

    def create_cnn_model(self):
        if self.config["CNN"]["backborn"] == "efficientnet":
            cnn_model = models.efficientnet_v2_s().to(self.device, non_blocking=True)
            cnn_model.classifier = nn.Linear(
                in_features=1280, out_features=self.config["CNN"]["classification"]
            ).to(self.device, non_blocking=True)
        elif self.config["CNN"]["backborn"] == "resnet":
            cnn_model = models.resnet101(pretrained=True).to(
                self.device, non_blocking=True
            )
            cnn_model.fc = nn.Linear(
                in_features=512, out_features=self.config["CNN"]["classification"]
            ).to(self.device, non_blocking=True)
        elif self.config["CNN"]["backborn"] == "mobilenet":
            cnn_model = models.mobilenet_v3_small().to(self.device, non_blocking=True)
            cnn_model.classifier[3] = nn.Linear(
                in_features=1024, out_features=self.config["CNN"]["classification"]
            ).to(self.device, non_blocking=True)
        device_ids = []
        for i in range(torch.cuda.device_count()):
            device_ids.append(i)
        cnn_model.load_state_dict(torch.load(self.MODEL_SAVE_PATH))
        cnn_model.to()
        cnn_model.eval()

        return cnn_model

    def evaluate_models(self):
        model.load_state_dict(torch.load(self.MODEL_SAVE_PATH))
        test_loss, test_acc = self.evaluate(
            model, self.device, valid_iterator, criterion
        )
        print(f"Test Loss: {test_loss:.3f} | Test Acc: {test_acc*100:.2f}% |")
        log_metric("Test Loss", f"{test_loss:.3f}")
        log_metric("Test Acc", f"{test_acc*100:.2f}")

    def transform_for_cnn(self):
        if self.config["CNN"]["backborn"] == "efficientnet":
            cnn_transforms = transforms.Compose(
                [transforms.Resize((384, 384)), transforms.ToTensor()]
            )
        elif self.config["CNN"]["backborn"] in ["resnet", "mobilenet"]:
            cnn_transforms = transforms.Compose(
                [transforms.Resize((224, 224)), transforms.ToTensor()]
            )

        return cnn_transforms

    def save_prediction(self, cnn_transforms, cnn_model):
        dir = f"{self.data_dir}/test/"
        file_lists = []

        for i in range(self.config["CNN"]["classification"]):
            file_lists.append(glob(f"{dir}/{i}*/*.*"))
        with open(f"{self.save_dir}eval.txt", "w") as f:
            for i in range(self.config["CNN"]["classification"]):
                print(self.config["TARGETS"][i], file=f)
                print(
                    self.predict_dir(file_lists[i], cnn_transforms, cnn_model),
                    file=f,
                )


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="./settings.yaml", type=str)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    train_cnn = CNNTrainer(args.config)
    set_experiment(train_cnn.config["EXPERIMENTS"]["mlflow"])
    with start_run(run_name=train_cnn.config["EXPERIMENTS"]["ver"]) as run:
        train_transforms, test_transforms = train_cnn.prepare_transform()
        train_data, valid_data, test_data = train_cnn.load_data()
        train_iterator, valid_iterator, test_iterator = train_cnn.shuffle_data(
            train_data, valid_data, test_data
        )
        model = train_cnn.build_model()
        optimizer, criterion, best_valid_loss, cls_weights = train_cnn.adjust_weights(
            model
        )
        train_cnn.log_params(cls_weights)
        train_cnn.train_cnn(optimizer, criterion, best_valid_loss)
        train_cnn.evaluate_models()
        cnn_transforms = train_cnn.transform_for_cnn()
        cnn_model = train_cnn.create_cnn_model()
        train_cnn.save_prediction(cnn_transforms, cnn_model)
