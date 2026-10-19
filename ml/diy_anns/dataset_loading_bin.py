import os
import torch
import random
from numpy import array
from PIL import Image
from transformers import AutoFeatureExtractor
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split

dataset_dir = os.environ.get('BINARY_DATASET_DIR', 'image_dataset_binary')
feature_extractor = AutoFeatureExtractor.from_pretrained("google/vit-base-patch16-224", trust_remote_code=True)
class_counts = {}

# Load data
data = {'image': [], 'label': []}
for label, class_dir in enumerate(os.listdir(dataset_dir)):
    class_dir_path = os.path.join(dataset_dir, class_dir)
    if os.path.isdir(class_dir_path):
        for img_file in os.listdir(class_dir_path):
            img_path = os.path.join(class_dir_path, img_file)
            image = Image.open(img_path).convert("RGB")
            image = feature_extractor(images=image, return_tensors="pt")['pixel_values'][0]
            data['image'].append(image.numpy())
            data['label'].append(label)

class_counts = dict((i, data['label'].count(i)) for i in data['label'])

# Identify the size of the smaller category
min_class_label = min(class_counts, key = class_counts.get)
min_class_size = class_counts[min_class_label]
max_class_label = max(class_counts, key = class_counts.get)
max_class_size = class_counts[max_class_label]

data_balanced = {'image': [], 'label': []}
max_cat_data = {'image': [], 'label': []}

random_index = random.sample(range(1, max_class_size), min_class_size)
for i in range(len(data['label'])):
    if data['label'][i] == min_class_label:
        data_balanced['image'].append(data['image'][i])
        data_balanced['label'].append(data['label'][i])
    else:
        max_cat_data['image'].append(data['image'][i])
        max_cat_data['label'].append(data['label'][i])

for i in random_index:
    data_balanced['image'].append(max_cat_data['image'][i])
    data_balanced['label'].append(max_cat_data['label'][i])



# Convert to Tensor
images = torch.tensor(data_balanced['image'])
labels = torch.tensor(data_balanced['label'])

# Split dataset
train_images, test_images, train_labels, test_labels = train_test_split(images, labels, test_size=0.2, stratify=labels)

# Create TensorDatasets and DataLoaders
train_dataset = TensorDataset(train_images, train_labels)
test_dataset = TensorDataset(test_images, test_labels)

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)
