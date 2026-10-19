import os
import torch
from PIL import Image
from transformers import AutoFeatureExtractor
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split

dataset_dir = os.environ.get('MULTIMODAL_DATASET_DIR', 'image_dataset_multimodal')
feature_extractor = AutoFeatureExtractor.from_pretrained("google/vit-base-patch16-224", trust_remote_code=True)

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

# Convert to Tensor
images = torch.tensor(data['image'])
labels = torch.tensor(data['label'])

# Split dataset
train_images, test_images, train_labels, test_labels = train_test_split(images, labels, test_size=0.2, stratify=labels)

# Create TensorDatasets and DataLoaders
train_dataset = TensorDataset(train_images, train_labels)
test_dataset = TensorDataset(test_images, test_labels)

train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)
