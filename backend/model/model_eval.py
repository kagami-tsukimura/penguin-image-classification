import os

import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms


def load_model(MODEL):
    PENGUIN_OUT = 7
    device, model = setting_backborn(PENGUIN_OUT)
    model.load_state_dict(torch.load(MODEL))
    model.eval()

    return device, model


def setting_backborn(out_features):
    device = torch.device("cpu" if is_production() else "cuda")

    model = models.efficientnet_v2_s(pretrained=True).to(device)
    for param in model.parameters():
        param.requires_grad = True
    model.classifier = nn.Linear(in_features=1280, out_features=out_features).to(
        device, non_blocking=True
    )

    return device, model


def prepare_data():
    test_transform = transforms.Compose(
        [transforms.Resize(((384, 384))), transforms.ToTensor()]
    )

    return test_transform


def eval_cnn(img, test_transform, model, device):
    test_img_tensor = test_transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(test_img_tensor)
        pred = torch.argmax(output).item()

    return pred


def judge_pred(pred):
    prediction = {
        0: "コウテイペンギン属",
        1: "アデリーペンギン属",
        2: "フンボルトペンギン属",
        3: "マカロニペンギン属",
        4: "キンメペンギン属",
        5: "コガタペンギン属",
        6: "その他",
    }

    dst = prediction.get(pred, "UNKNOWN")

    return dst


def is_production():
    return os.environ.get("ENV", None) is not None
