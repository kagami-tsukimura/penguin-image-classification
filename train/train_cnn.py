import argparse
import os
from datetime import datetime
from glob import glob

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image, ImageFile
from torch.autograd import Variable
from torch.utils.data import DataLoader
from tqdm import tqdm


class TrainCNN:
    def __init__(self, setting_path) -> None:
        self.SETTING_PATH = setting_path
        date = datetime.now()
        os.makedirs(self.save_dir, exist_ok=True)
        self.save_dir = f"{self.save_dir}/"
        self.device = torch.device("cuda")
        EXPERIMENTS = {"ver": "r0", "mlflow": "penguin"}
        PREPARE = {"batch_size": 16}
        CNN = {
            "mode": "penguin",
            "seed": 42,
            "backborn": "efficientnet",  # または 'resnet'
            "epoch": 50,
            "classification": 7,
        }
        TARGETS = [
            "Aptenodytes",
            "Pygoscelis",
            "Spheniscus",
            "Eudyptes",
            "Megadyptes",
            "Eudyptula",
            "Other",
        ]
        WEIGHTS = {"automation": True, "classes": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]}
        PATH = {"work": "./", "model": "model", "data": "data/penguins"}

    def setting_transform(self):
        train_transforms = transforms.Compose(
            [
                transforms.RandomChoice(
                    [
                        transforms.Resize((448, 448)),
                        transforms.Resize((416, 416)),
                        transforms.Resize((400, 400)),
                    ]
                ),
                [
                    transforms.RandomCrop((384, 384)),
                    transforms.Resize((384, 384)),
                    transforms.ToTensor(),
                ],
            ]
        )
        test_transforms = transforms.Compose(
            [
                transforms.Resize((384, 384)),
                transforms.ToTensor(),
            ]
        )

        return train_transforms, test_transforms

    def fetch_data(self):
        train_data = datasets.ImageFolder(f"{self.data_dir}/train", train_transforms)
        valid_data = datasets.ImageFolder(f"{self.data_dir}/test", test_transforms)
        test_data = datasets.ImageFolder(f"{self.data_dir}/test", test_transforms)

        return train_data, valid_data, test_data

    def setting_backborn(self):
        model = models.efficientnet_v2_s(pretrained=True).to(
            self.device, non_blocking=True
        )
        for param in model.parameters():
            param.requires_grad = True
        model.classifier = nn.Linear(in_features=1280, out_features=7).to(
            self.device, non_blocking=True
        )

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

    def predict_image(self, image, cnn_transforms, cnn_model):
        image_tensor = cnn_transforms(image).float()
        image_tensor = image_tensor.unsqueeze_(0)
        input = Variable(image_tensor)
        input = input.to(self.device, non_blocking=True)
        output = cnn_model(input)
        index = output.data.cpu().numpy().argmax()

        return index

    def predict_dir(self, fileList, cnn_transforms, cnn_model):
        results = []
        for file in fileList:
            img = Image.open(file).convert("RGB")
            idx = self.predict_image(img, cnn_transforms, cnn_model)
            results[idx] += 1

        return results

    def adjust_weights(self, model):
        optimizer = optim.Adam(model.parameters())
        weights = torch.tensor([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.2]).cuda()
        criterion = nn.CrossEntropyLoss(weight=weights)
        best_valid_loss = float("inf")

        return optimizer, criterion, best_valid_loss

    def train_cnn(self, optimizer, criterion, best_valid_loss):
        for epoch in range(self.EPOCHS):
            train_loss, train_acc = train_cnn.train(
                model, self.device, train_iterator, optimizer, criterion
            )
            valid_loss, valid_acc = train_cnn.evaluate(
                model, self.device, valid_iterator, criterion
            )

            if valid_loss < best_valid_loss:
                best_valid_loss = valid_loss
                torch.save(model.state_dict(), self.MODEL_SAVE_PATH)
            torch.save(model.state_dict(), self.MODEL_SAVE_PATH2)

    def setting_cnn_model(self):
        cnn_model = models.efficientnet_v2_s().to(self.device, non_blocking=True)
        cnn_model.classifier = nn.Linear(in_features=1280, out_features=7).to(
            self.device, non_blocking=True
        )
        device_ids = []
        for i in range(torch.cuda.device_count()):
            device_ids.append(i)
        cnn_model.load_state_dict(torch.load(self.MODEL_SAVE_PATH))
        cnn_model.to()
        cnn_model.eval()

        return cnn_model

    def cnn_trans(self):
        cnn_transforms = transforms.Compose(
            [transforms.Resize((384, 384)), transforms.ToTensor()]
        )

        return cnn_transforms


def setting_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="./settings.yaml", type=str)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = setting_args()
    train_cnn = TrainCNN(args.config)
    train_transforms, test_transforms = train_cnn.setting_transform()
    train_data, valid_data, test_data = train_cnn.fetch_data()
    model = train_cnn.setting_backborn()
    optimizer, criterion, best_valid_loss = train_cnn.adjust_weights(model)
    train_cnn.train_cnn(optimizer, criterion, best_valid_loss)
    cnn_transforms = train_cnn.cnn_trans()
    cnn_model = train_cnn.setting_cnn_model()
