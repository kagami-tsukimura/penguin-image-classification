import torch
import torch.nn as nn
import torchvision.models as models


def load_model(MODEL):
    PENGUIN_OUT = 7
    model = setting_backborn(PENGUIN_OUT)
    model.load_state_dict(torch.load(MODEL))
    model.eval()

    return model


def setting_backborn(out_features):
    device = torch.device("cuda")

    model = models.efficientnet_v2_s(pretrained=True).to(device)
    for param in model.parameters():
        param.requires_grad = True
    model.classifier = nn.Linear(in_features=1280, out_features=out_features).to(
        device, non_blocking=True
    )

    return model
