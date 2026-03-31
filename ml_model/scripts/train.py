import argparse
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


CLASS_NAMES = ["plastic", "metal", "organic"]


def build_model(num_classes: int = 3):
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.3),
        nn.Linear(in_features, num_classes),
    )
    return model


def train(data_dir: Path, model_out: Path, epochs: int = 10, batch_size: int = 16):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )

    train_dataset = datasets.ImageFolder(data_dir / "train", transform=transform)
    val_dataset = datasets.ImageFolder(data_dir / "val", transform=transform)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)

    model = build_model(num_classes=len(train_dataset.classes)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-4)

    best_acc = 0.0
    model_out.parent.mkdir(parents=True, exist_ok=True)

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        model.eval()
        correct, total = 0, 0
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        acc = correct / total if total else 0
        print(f"Epoch {epoch+1}/{epochs} - loss={running_loss/len(train_loader):.4f} - val_acc={acc:.4f}")

        if acc > best_acc:
            best_acc = acc
            torch.save(
                {"model_state_dict": model.state_dict(), "classes": train_dataset.classes},
                model_out,
            )
            print(f"Saved best model to {model_out}")

    print(f"Training finished. Best validation accuracy: {best_acc:.4f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train waste classifier (Plastic/Metal/Organic)")
    parser.add_argument("--data-dir", type=Path, default=Path("ml_model/data/trashnet"))
    parser.add_argument("--model-out", type=Path, default=Path("ml_model/models/waste_classifier.pt"))
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=16)
    args = parser.parse_args()

    train(args.data_dir, args.model_out, args.epochs, args.batch_size)
