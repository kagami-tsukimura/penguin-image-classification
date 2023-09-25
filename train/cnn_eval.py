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
