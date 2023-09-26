import os
import subprocess
from glob import glob

import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
import yaml
from PIL import Image, ImageFile
from tqdm import tqdm


def setting_backborn():
    device = torch.device("cuda")
    config = load_settings()

    if config["CNN"]["backborn"] == "efficientnet":
        model = models.efficientnet_v2_s(pretrained=True).to(device)
        for param in model.parameters:
            param.requires_grad = True
        model.classifier = nn.Linear(
            in_features=1280, out_features=config["CNN"]["classification"]
        ).to(device, non_blocking=True)
    elif config["CNN"]["backborn"] == "resnet":
        model = models.resnet101(pretrained=True).to(device, non_blocking=True)
        for param in model.parameters:
            param.requires_grad = True
        model.fc = nn.Linear(
            in_features=512, out_features=config["CNN"]["classification"]
        ).to(device, non_blocking=True)

    return model


def load_settings():
    with open("./settings.yaml", "r") as f:
        return yaml.safe_load(f)


def mkdirs(dirs):
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)


def prepare_data():
    test_transform = transforms.Compose(
        [transforms.Resize(((384, 384))), transforms.ToTensor()]
    )

    return test_transform


def eval_cnn(img, test_transform, model):
    test_img = Image.open(img).convert("RGB")
    test_img_tensor = test_transform(test_img).unsqueeze(0)
    model.eval()
    with torch.no_grad():
        output = model(test_img_tensor)
        pred = torch.argmax(output).item()

    return pred


def judge_pred(pred, dirs):
    # TODO: refactor
    if pred == 0:
        dst_dir = dirs[0]
    elif pred == 1:
        dst_dir = dirs[1]
    elif pred == 2:
        dst_dir = dirs[2]
    elif pred == 3:
        dst_dir = dirs[3]
    elif pred == 4:
        dst_dir = dirs[4]
    elif pred == 5:
        dst_dir = dirs[5]
    elif pred == 6:
        dst_dir = dirs[6]

    return dst_dir


def mv_file(img, dst_dir):
    cmd = f"mv {img} {dst_dir}"
    subprocess.check_call(cmd.split())


def main():
    MODEL = "./weights/efficientnet-penguin-7cls.pt"
    LABEL_PATH = "./data/edit/"
    DIRS = [
        f"{LABEL_PATH}/0Aptenodytes",
        f"{LABEL_PATH}/1Pygoscelis",
        f"{LABEL_PATH}/2Spheniscus",
        f"{LABEL_PATH}/3Eudyptes",
        f"{LABEL_PATH}/4Megadyptes",
        f"{LABEL_PATH}/5Eudyptula",
        f"{LABEL_PATH}/6Other",
    ]

    model = setting_backborn()
    model.load_state_dict(torch.load(MODEL))
    imgs = glob(f"{LABEL_PATH}/*.*")
    mkdirs(DIRS)
    # NOTE: Make sure you can read large sized images.
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    test_transform = prepare_data()
    for img in tqdm(imgs):
        pred = eval_cnn(img, test_transform, model)
        dst_dir = judge_pred(pred, DIRS)
        mv_file(img, dst_dir)


if __name__ == "__main__":
    main()
