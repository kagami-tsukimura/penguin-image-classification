import argparse

import torchvision.transforms as transforms


class TrainCNN:
    def __init__(self, setting_path) -> None:
        pass

    def setting_transforms(self):
        train_transforms = transforms.Compose(
            [
                transforms.RandomHorizontalFlip(),
                transforms.RandomChoice(
                    [
                        transforms.ColorJitter(
                            brightness=0.5, contrast=0.2, saturation=0.2
                        ),
                        transforms.RandomRotation(10),
                    ]
                ),
                transforms.RandomChoice(
                    [
                        transforms.RandomCrop((300, 300)),
                        transforms.RandomCrop((280, 280)),
                        transforms.RandomCrop((240, 240)),
                    ]
                ),
                transforms.RandomCrop((224, 224)),
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
            ]
        )
        test_transforms = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
            ]
        )
        return train_transforms, test_transforms


def setting_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="./setting.yaml", type=str)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = setting_args()
    train_cnn = TrainCNN(args.config)
    train_transforms, test_transforms = train_cnn.setting_transforms()
