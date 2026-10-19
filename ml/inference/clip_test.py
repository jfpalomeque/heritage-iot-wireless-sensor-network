import os
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import torch

# Load the model and processor
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# Define the dataset path
dataset_path = r"path_to_your_dataset_folder"

# Define labels (from subfolder names)
labels = os.listdir(dataset_path)

# Initialize counters
total_images = 0
correct_predictions = 0

# Iterate through each label folder
for label in labels:
    label_folder = os.path.join(dataset_path, label)
    if os.path.isdir(label_folder):
        # Iterate through each image in the label folder
        for image_name in os.listdir(label_folder):
            image_path = os.path.join(label_folder, image_name)
            image = Image.open(image_path)

            # Process the image with CLIP
            inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)
            outputs = model(**inputs)
            logits_per_image = outputs.logits_per_image
            probs = logits_per_image.softmax(dim=1)  # Get probabilities

            # Get the predicted label
            predicted_index = torch.argmax(probs, dim=1).item()
            predicted_label = labels[predicted_index]

            # Compare the predicted label with the actual label (folder name)
            if predicted_label == label:
                correct_predictions += 1
            total_images += 1

# Calculate accuracy
accuracy = correct_predictions / total_images
print(f"Accuracy: {accuracy:.4f}")
print(f"Correct Predictions: {correct_predictions}")
print(f"Total Images: {total_images}")
