"""Run a local Hugging Face image-classification checkpoint on one image."""

import argparse

import torch
from PIL import Image
from transformers import AutoFeatureExtractor, AutoModelForImageClassification


def predict(model_path: str, image_path: str) -> int:
    model = AutoModelForImageClassification.from_pretrained(model_path)
    feature_extractor = AutoFeatureExtractor.from_pretrained(model_path)
    image = Image.open(image_path).convert("RGB")
    inputs = feature_extractor(images=image, return_tensors="pt")
    model.eval()
    with torch.no_grad():
        return model(**inputs).logits.argmax(-1).item()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model_path", help="directory containing a released checkpoint")
    parser.add_argument("image_path", help="image to classify")
    args = parser.parse_args()
    print(f"Predicted class index: {predict(args.model_path, args.image_path)}")
