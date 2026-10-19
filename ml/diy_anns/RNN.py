import torch
import torch.nn as nn
import torch.optim as optim
import time

class SimpleRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleRNN, self).__init__()
        self.hidden_size = hidden_size
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        h0 = torch.zeros(1, x.size(0), self.hidden_size).to(x.device)  # Initialize hidden state
        out, _ = self.rnn(x, h0)
        out = self.fc(out[:, -1, :])
        return out

# Assuming images are of size (batch_size, 3, 224, 224)
input_size = 224 * 3  # Each row of pixels is treated as a time step, with 3 channels
hidden_size = 128
output_size = len(set(data['label']))
learning_rate = 0.001
num_epochs = 5

# Initialize the network, loss function, and optimizer
model = SimpleRNN(input_size, hidden_size, output_size)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

start = time.time()

# Training loop
for epoch in range(num_epochs):
    model.train()
    for images, labels in train_loader:
        images = images.view(images.size(0), images.size(2), -1)  # Reshape to (batch_size, seq_len, input_size)
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
            images = images.view(images.size(0), images.size(2), -1)  # Reshape to (batch_size, seq_len, input_size)
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
