import torch.nn as nn
import torch.optim as optim
import time

# Define the neural network
class SimpleFNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleFNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = x.view(x.size(0), -1)  # Flatten the input
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out

# Hyperparameters
input_size = images.shape[1] * images.shape[2] * images.shape[3]  # Flattened image size
hidden_size = 500
output_size = len(set(data['label']))
learning_rate = 0.001
num_epochs = 5

# Initialize the network, loss function, and optimizer
model = SimpleFNN(input_size, hidden_size, output_size)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

start = time.time()

# Training loop
for epoch in range(num_epochs):
    model.train()
    for images, labels in train_loader:
        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Evaluation loop
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in test_loader:
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total

    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}, Accuracy: {accuracy:.2f}%')
end = time.time()
time_diff = end - start
hours, rem = divmod(time_diff, 3600)
hours = int(hours)
minutes, seconds = divmod(rem, 60)
minutes = int(minutes)
seconds = round(seconds, 3)
print(f"Execution time of training: {hours}:{minutes}:{seconds}")
