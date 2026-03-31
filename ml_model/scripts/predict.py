import argparse
from pathlib import Path

import torch
from PIL import Image
from torchvision import models, transforms


def load_model(model_path: Path):
    checkpoint = torch.load(model_path, map_location="cpu")
    classes = checkpoint["classes"]

    model = models.resnet18(weights=None)
    model.fc = torch.nn.Sequential(
        torch.nn.Dropout(0.3),
        torch.nn.Linear(model.fc.in_features, len(classes)),
    )
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model, classes


def predict_image(model, classes, image_path: Path):
    tfm = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    image = Image.open(image_path).convert("RGB")
    tensor = tfm(image).unsqueeze(0)

    with torch.no_grad():
        logits = model(tensor)
        probs = torch.softmax(logits, dim=1)[0]
        confidence, predicted_idx = torch.max(probs, dim=0)

    return classes[predicted_idx.item()], confidence.item()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict waste class from image")
    parser.add_argument("--model-path", type=Path, default=Path("ml_model/models/waste_classifier.pt"))
    parser.add_argument("--image-path", type=Path, required=True)
    args = parser.parse_args()

    model, classes = load_model(args.model_path)
    label, confidence = predict_image(model, classes, args.image_path)
    print({"label": label, "confidence": round(confidence, 4)})
