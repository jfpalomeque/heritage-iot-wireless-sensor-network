from PIL import Image
import requests
import time
import csv
import json
import torch
from transformers import CLIPProcessor, CLIPModel, AutoModelForImageClassification, AutoFeatureExtractor
from PIL import Image
import time
from transformers import CLIPProcessor, CLIPModel

def CLIP_analyze_image(image_file, image_labels_file):

    model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

    image = Image.open(image_file)

    with open(image_labels_file, 'r') as f:
        labels_data = json.load(f)



    positive_labels = labels_data["free_positive_labels"]
    negative_labels = labels_data["free_negative_labels"]
    labels = positive_labels + negative_labels
    inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)

    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)

    values_list = probs[0].tolist()


    label_prob_pairs = list(zip(labels, values_list))


    positive_sum = sum(prob for label, prob in label_prob_pairs if label in positive_labels)
    negative_sum = sum(prob for label, prob in label_prob_pairs if label in negative_labels)

    if negative_sum >= positive_sum:
        return "negative", "CLIP"
    if negative_sum < positive_sum:
        return "positive", "CLIP"
    else:
        return None, "CLIP"

def VIT_analyze_image_multilabel(image_path, image_labels_file, model_path):


    model = AutoModelForImageClassification.from_pretrained(model_path)
    feature_extractor = AutoFeatureExtractor.from_pretrained(model_path)

    # Function to preprocess the image
    def preprocess_image(image_path):
        image = Image.open(image_path).convert("RGB")
        inputs = feature_extractor(images=image, return_tensors="pt")
        return inputs['pixel_values']


    def predict(image_path):
        model.eval()
        inputs = preprocess_image(image_path)
        with torch.no_grad():
            outputs = model(inputs)
        logits = outputs.logits
        predicted_class_idx = logits.argmax(-1).item()
        return predicted_class_idx

    predicted_class = predict(image_path)

    with open(image_labels_file, 'r') as f:
        labels_data = json.load(f)

    multilabels = labels_data['closed_labels']

    predicted_class_label = multilabels[str(predicted_class)]

    positive_closed_labels = labels_data["closed_positive_labels"]
    negative_closed_labels = labels_data["closed_negative_labels"]

    if predicted_class_label in positive_closed_labels:
        return "positive", "VIT_fine_tuned"
    if predicted_class_label in negative_closed_labels:
        return "negative", "VIT_fine_tuned"
    else:
        return None, "VIT_fine_tuned"
