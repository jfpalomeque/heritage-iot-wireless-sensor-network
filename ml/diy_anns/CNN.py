import torch.nn as nn
import torch.optim as optim
import time

class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=3, out_channels=16, kernel_size=5, stride=1, padding=2)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2, padding=0)
        self.conv2 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=5, stride=1, padding=2)
        self.fc1 = nn.Linear(32 * 56 * 56, 1000)  # Adjust based on your image size after convolutions
        self.fc2 = nn.Linear(1000, output_size)

    def forward(self, x):
        x = self.pool(torch.relu(self.conv1(x)))
        x = self.pool(torch.relu(self.conv2(x)))
        x = x.view(-1, 32 * 56 * 56)  # Adjust based on your image size after convolutions
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# Hyperparameters
learning_rate = 0.001
num_epochs = 5

# Initialize the network, loss function, and optimizer
model = SimpleCNN()
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
