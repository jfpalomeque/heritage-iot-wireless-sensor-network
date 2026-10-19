import argparse
from PIL import Image
import time

from transformers import CLIPProcessor, CLIPModel

start = time.time()

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

parser = argparse.ArgumentParser()
parser.add_argument("image_path", help="image to classify")
args = parser.parse_args()
image_path = args.image_path
image = Image.open(image_path)

positive_labels = [
    "walking", "observing exhibits", "reading information plaques",
    "taking photos", "calm"
]


negative_labels = [
    "running", "eating", "drinking", "touching exhibits", "violent", "problematic", "carrying a blunt object"
]

labels = positive_labels + negative_labels



inputs = processor(text=labels, images=image, return_tensors="pt", padding=True)

outputs = model(**inputs)
logits_per_image = outputs.logits_per_image # this is the image-text similarity score
probs = logits_per_image.softmax(dim=1) # we can take the softmax to get the label probabilities

values_list = probs[0].tolist()

# Combine the labels and probabilities into a list of tuples
label_prob_pairs = list(zip(labels, values_list))

# Sort the list of tuples by the probability in descending order
sorted_label_prob_pairs = sorted(label_prob_pairs, key=lambda x: x[1], reverse=True)

# Calculate the sum of probabilities for positive and negative labels
positive_sum = sum(prob for label, prob in label_prob_pairs if label in positive_labels)
negative_sum = sum(prob for label, prob in label_prob_pairs if label in negative_labels)


# Print the sorted probabilities along with their corresponding labels
for label, prob in sorted_label_prob_pairs:
    print(f"{label}: {prob:.4f}")

print(f"\nSum of positive label probabilities: {positive_sum:.4f}")
print(f"Sum of negative label probabilities: {negative_sum:.4f}")


end = time.time()
print(f"Time: {end - start:.2f} seconds")
