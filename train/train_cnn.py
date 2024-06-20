import argparse
import os
import random
from datetime import datetime
from glob import glob
from pathlib import Path

import numpy as np
import optuna
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.datasets as datasets
import torchvision.models as models
import torchvision.transforms as transforms
import yaml
from mlflow import (
    create_experiment,
    get_experiment_by_name,
    log_artifact,
    log_metric,
    log_param,
    log_params,
    set_experiment,
    set_tracking_uri,
    start_run,
)
from mlflow.pytorch import log_model
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
        self.datetime = date.strftime("%Y%m%d%H%M")
        self.save_dir = (
            f"{work_dir}{self.datetime}_{self.config['EXPERIMENTS']['ver']}/"
        )
        os.makedirs(self.save_dir, exist_ok=True)
        SAVE_DIR = self.config["PATH"]["model"]
        CNN_FILE = f"{self.config['CNN']['backborn']}-{self.config['CNN']['mode']}-{self.config['CNN']['classification']}cls.pt"
        self.MODEL_SAVE_PATH = f"{self.save_dir}{CNN_FILE}"
        self.MODEL_SAVE_PATH2 = Path(f"{SAVE_DIR}/{CNN_FILE}")
        os.makedirs(SAVE_DIR, exist_ok=True)
        self.device = torch.device("cuda")
        self.dropout = self.config["CNN"]["dropout"]
        self.lr = self.config["CNN"]["lr"]
        self.weight_decay = self.config["CNN"]["weight_decay"]
        self.batch_size = self.config["PREPARE"]["batch_size"]

    def load_settings(self):
        with open(self.CONFIG_PATH, "r") as f:
            return yaml.safe_load(f)

    def create_hpo_params(self):
        # Optunaスタディの作成
        study = optuna.create_study(direction=self.config["CNN"]["direction"])
        study.optimize(self.objective, n_trials=self.config["CNN"]["n_trials"])

        print("Best trial:")
        trial = study.best_trial

        print(f"  Value: {trial.value}")
        print("  Params: ")
        for key, value in trial.params.items():
            print(f"    {key}: {value}")

        # 最適なハイパーパラメータを使って再度トレーニング
        self.dropout = trial.params["dropout"]
        self.lr = trial.params["lr"]
        self.weight_decay = trial.params["weight_decay"]
        self.batch_size = trial.params["batch_size"]

    def objective(self, trial):
        # ハイパーパラメータの提案
        dropout_rate = trial.suggest_float("dropout", 0.2, 0.5)
        lr = trial.suggest_loguniform("lr", 1e-5, 1e-2)
        weight_decay = trial.suggest_loguniform("weight_decay", 1e-5, 1e-2)
        batch_size = trial.suggest_categorical("batch_size", [32, 64, 128])

        # 設定を更新
        self.dropout = dropout_rate
        self.lr = lr
        self.weight_decay = weight_decay
        self.batch_size = batch_size

        # データの準備
        train_transforms, test_transforms = self.prepare_transform()
        train_data, valid_data, test_data = self.load_data()
        train_iterator, valid_iterator, test_iterator = self.shuffle_data(
            train_data, valid_data, test_data
        )

        # モデルとオプティマイザの設定
        model = self.build_model()
        optimizer, criterion, best_valid_loss, cls_weights = self.adjust_weights(model)

        # トレーニングと評価
        for epoch in range(self.config["CNN"]["hpo_epoch"]):
            train_loss, train_acc = self.train(
                model, self.device, train_iterator, optimizer, criterion
            )
            valid_loss, valid_acc = self.evaluate(
                model, self.device, valid_iterator, criterion
            )

            print(
                f"| Epoch: {epoch+1:02} | Train Loss: {train_loss:.3f} | Train Acc: {train_acc*100:.2f}% | Val. Loss: {valid_loss:.3f} | Val. Acc: {valid_acc*100:.2f}% |"  # noqa
            )

            # Early stoppingのためのプルーニングチェック
            trial.report(valid_loss, epoch)
            if trial.should_prune():
                raise optuna.exceptions.TrialPruned()

        return valid_loss

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

    def load_data(self, is_train=False):
        train_transforms, test_transforms = self.prepare_transform()
        train_data = datasets.ImageFolder(f"{self.data_dir}/train", train_transforms)
        valid_data = datasets.ImageFolder(f"{self.data_dir}/test", test_transforms)
        test_data = datasets.ImageFolder(f"{self.data_dir}/test", test_transforms)
        if is_train:
            print(f"Number of training data: {len(train_data)}")
            print(f"Number of validation data: {len(valid_data)}")
            print(f"Number of testing data: {len(test_data)}")

        return train_data, valid_data, test_data

    def shuffle_data(self, train_data, valid_data, test_data):
        BATCH_SIZE = self.batch_size
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
            model.classifier = nn.Sequential(
                nn.Dropout(p=self.dropout),
                nn.Linear(
                    in_features=1280, out_features=self.config["CNN"]["classification"]
                ).to(self.device, non_blocking=True),
            )
        elif self.config["CNN"]["backborn"] == "resnet":
            model = models.resnet101(pretrained=True).to(self.device, non_blocking=True)
            for param in model.parameters():
                param.requires_grad = True
            model.fc = nn.Sequential(
                nn.Dropout(p=self.dropout),
                nn.Linear(
                    in_features=2048, out_features=self.config["CNN"]["classification"]
                ).to(self.device, non_blocking=True),
            )
        elif self.config["CNN"]["backborn"] == "resnet34":
            model = models.resnet34(pretrained=True).to(self.device, non_blocking=True)
            for param in model.parameters():
                param.requires_grad = True
            model.fc = nn.Sequential(
                nn.Dropout(p=self.dropout),
                nn.Linear(
                    in_features=512, out_features=self.config["CNN"]["classification"]
                ).to(self.device, non_blocking=True),
            )
        elif self.config["CNN"]["backborn"] == "mobilenet":
            model = models.mobilenet_v3_small(pretrained=True).to(
                self.device, non_blocking=True
            )
            for param in model.parameters():
                param.requires_grad = True
            model.classifier[3] = nn.Sequential(
                nn.Dropout(p=self.dropout),
                nn.Linear(
                    in_features=1024, out_features=self.config["CNN"]["classification"]
                ).to(self.device, non_blocking=True),
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

    def adjust_weights(self, model, is_train=False):
        optimizer = optim.Adam(
            model.parameters(),
            lr=self.lr,
            weight_decay=self.weight_decay,
        )
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

        if is_train:
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
                "batch_size": self.batch_size,
                "mode": self.config["CNN"]["mode"],
                "seed": self.config["CNN"]["seed"],
                "backborn": self.config["CNN"]["backborn"],
                "epoch": self.config["CNN"]["epoch"],
                "lr": self.lr,
                "weight_decay": self.weight_decay,
                "dropout": self.dropout,
                "hpo": self.config["CNN"]["hpo"],
                "n_trials": self.config["CNN"]["n_trials"],
                "train_data": f"{self.data_dir}/train",
                "valid_data": f"{self.data_dir}/test",
                "test_data": f"{self.data_dir}/test",
            }
        )
        for i in range(self.config["CNN"]["classification"]):
            log_param(f"{i}{self.config['TARGETS'][i]}", cls_weights[i])

    def train_cnn(self, optimizer, criterion, best_valid_loss):
        CHECKPOINT = self.config["CNN"]["checkpoint"]
        CHECKPOINT_DIR = Path(f"{self.save_dir}/checkpoints")
        CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

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

            # checkpointの保存
            if (epoch + 1) % CHECKPOINT == 0:
                checkpoint_path = (
                    CHECKPOINT_DIR
                    / f"epoch-{epoch+1}-{self.config['CNN']['backborn']}-{self.config['CNN']['mode']}-{self.config['CNN']['classification']}cls.pt"
                )
                torch.save(model.state_dict(), checkpoint_path)

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
            cnn_model.classifier = nn.Sequential(
                nn.Dropout(p=self.dropout),
                nn.Linear(
                    in_features=1280, out_features=self.config["CNN"]["classification"]
                ).to(self.device, non_blocking=True),
            )
        elif self.config["CNN"]["backborn"] == "resnet":
            cnn_model = models.resnet101(pretrained=True).to(
                self.device, non_blocking=True
            )
            cnn_model.fc = nn.Sequential(
                nn.Dropout(p=self.dropout),
                nn.Linear(
                    in_features=2048, out_features=self.config["CNN"]["classification"]
                ).to(self.device, non_blocking=True),
            )
        elif self.config["CNN"]["backborn"] == "resnet34":
            cnn_model = models.resnet34(pretrained=True).to(
                self.device, non_blocking=True
            )
            cnn_model.fc = nn.Sequential(
                nn.Dropout(p=self.dropout),
                nn.Linear(
                    in_features=512, out_features=self.config["CNN"]["classification"]
                ).to(self.device, non_blocking=True),
            )
        elif self.config["CNN"]["backborn"] == "mobilenet":
            cnn_model = models.mobilenet_v3_small().to(self.device, non_blocking=True)
            cnn_model.classifier[3] = nn.Sequential(
                nn.Dropout(p=self.dropout),
                nn.Linear(
                    in_features=1024, out_features=self.config["CNN"]["classification"]
                ).to(self.device, non_blocking=True),
            )
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
        elif self.config["CNN"]["backborn"] in ["resnet", "resnet34", "mobilenet"]:
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

    def save_artifacts(self, config, model):
        log_artifact(os.path.basename(__file__))
        log_artifact(self.save_dir)
        log_artifact(config)
        log_model(model, "model")


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c",
        "--config",
        default="./settings.yaml",
        type=str,
        help="Path to the configuration file.",
    )
    parser.add_argument(
        "-p", "--checkpoint_path", type=str, help="Path to the checkpoint file."
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()
    train_cnn = CNNTrainer(args.config)

    # SageMakerユーザーならFargate上のMLflowに保存
    if os.uname()[1] == "default":
        set_tracking_uri(train_cnn.config["MLFLOW"]["tracking_uri"])
        experiment = get_experiment_by_name(train_cnn.config["EXPERIMENTS"]["mlflow"])
        if experiment is None:
            create_experiment(
                name=train_cnn.config["EXPERIMENTS"]["mlflow"],
                artifact_location=f"{train_cnn.config['MLFLOW']['artifact_uri']}/{train_cnn.config['EXPERIMENTS']['mlflow']}/",
            )

    set_experiment(train_cnn.config["EXPERIMENTS"]["mlflow"])

    with start_run(run_name=train_cnn.config["EXPERIMENTS"]["ver"]) as run:
        if train_cnn.config["CNN"]["hpo"]:
            train_cnn.create_hpo_params()

        train_transforms, test_transforms = train_cnn.prepare_transform()
        train_data, valid_data, test_data = train_cnn.load_data(is_train=True)
        train_iterator, valid_iterator, test_iterator = train_cnn.shuffle_data(
            train_data, valid_data, test_data
        )
        model = train_cnn.build_model()
        optimizer, criterion, best_valid_loss, cls_weights = train_cnn.adjust_weights(
            model, is_train=True
        )
        train_cnn.log_params(cls_weights)

        # Load checkpoint if specified
        if args.checkpoint_path:
            model.load_state_dict(torch.load(args.checkpoint_path))
            print(f"Resume training from checkpoint: {args.checkpoint_path}")

        train_cnn.train_cnn(optimizer, criterion, best_valid_loss)
        train_cnn.evaluate_models()
        cnn_transforms = train_cnn.transform_for_cnn()
        cnn_model = train_cnn.create_cnn_model()
        train_cnn.save_prediction(cnn_transforms, cnn_model)
        train_cnn.save_artifacts(args.config, model)
