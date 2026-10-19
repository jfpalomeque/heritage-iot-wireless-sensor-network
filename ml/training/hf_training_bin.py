from transformers import AutoModelForImageClassification, AutoFeatureExtractor, TrainingArguments, Trainer
from datasets import load_metric, Dataset, DatasetDict
from sklearn.model_selection import train_test_split
import torch
from torchvision.transforms import Compose, Resize, CenterCrop, ToTensor, Normalize
from PIL import Image
import os
import pandas as pd
import time
import json

type_classificator = 'binary'

dataset_dir = 'image_dataset_binary'
feature_extractor = AutoFeatureExtractor.from_pretrained("google/vit-base-patch16-224")

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

# Check the number of items in the smalles label group, and select randomly an equal size sample from the biggest label group, balancing the sample sizes
label_counts = pd.Series(data['label']).value_counts()
min_label_count = label_counts.min()
data_balanced = {'image': [], 'label': []}
for label in label_counts.index:
    label_data = [data['image'][i] for i in range(len(data['label'])) if data['label'][i] == label]
    label_data = label_data[:min_label_count]
    data_balanced['image'].extend(label_data)
    data_balanced['label'].extend([label] * len(label_data))

dataset = Dataset.from_dict(data_balanced)
size = 0.8
results = {}
num_labels = len(set(dataset['label']))

# Transform function
def transform(examples):
    examples['pixel_values'] = examples['image']
    return examples

dataset = dataset.with_transform(transform)


start = time.time()
df = pd.DataFrame(dataset)
train_df, test_df = train_test_split(df, train_size = size, stratify =df['label'])
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)
subset = DatasetDict({'train': train_dataset, 'test': test_dataset})

# Training function
def train_and_evaluate(dataset, model_name, num_labels, training_args):
    model = AutoModelForImageClassification.from_pretrained(model_name, num_labels=num_labels, ignore_mismatched_sizes=True)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=dataset['train'],
        eval_dataset=dataset['test'],
        compute_metrics=compute_metrics,
    )

    trainer.train()
    results = trainer.evaluate()

    trainer.save_model(output_dir)
    feature_extractor.save_pretrained(output_dir)

    return results

metric = load_metric("accuracy")

def compute_metrics(p):
    return metric.compute(predictions=p.predictions.argmax(-1), references=p.label_ids)

training_args = TrainingArguments(
    output_dir=f"./hf_output/results_{type_classificator}_{int(size*100)}",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=5,
    weight_decay=0.01,
)

output_dir = f"./hf_output/model_{type_classificator}_{int(size*100)}"

print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
print(f"Training with {int(size*100)}% of the dataset")
result = train_and_evaluate(subset, "google/vit-base-patch16-224", num_labels, training_args)
end = time.time()
time_diff = end - start
hours, rem = divmod(time_diff, 3600)
hours = int(hours)
minutes, seconds = divmod(rem, 60)
minutes = int(minutes)
seconds = round(seconds, 3)
print(f"Execution time of training with {int(size*100)}% of the dataset: {hours}:{minutes}:{seconds}")
result['runtime'] = f'{hours}:{minutes}:{seconds}'
results[f"{int(size*100)}%"] = result
print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

print(results)
