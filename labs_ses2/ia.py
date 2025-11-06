import torch #type: ignore
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import cv2 
import platform

nn = torch.nn

class IA:
    NB_CLASSES = 2 
    LEARNING_RATE = 0.001
    BATCH_SIZE = 32
    NUM_EPOCHS = 10
    
    def __init__(self):
        self.model = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(32 * 32 * 32, 128),
            nn.ReLU(),
            nn.Linear(128, num_classes)
        )
    
    def entrainer(self, dossier_train):
        transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
        ])
        train = datasets.ImageFolder(platform.os.path.join(dossier_train), transform=transform)
        train_loader = DataLoader(train, self.BATCH_SIZE, shuffle=True)
        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        criterion = nn.CrossEntropyLoss()					# Fonction de coût
        optimizer = optim.Adam(modele.parameters(), lr=learning_rate)		# Descente de gradient
        modele.to(device)
        modele.train()
        for epoch in range(num_epochs):
            total_loss, correct = 0, 0
            for images, labels in train_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = modele(images)
                loss = criterion(outputs, labels)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
                correct += (outputs.argmax(1) == labels).sum().item() # Nombre de prédictions correctes dans un batch  
                acc = 100 * correct / len(train_loader.dataset)
            print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}, Accuracy: {acc:.2f}%")

        