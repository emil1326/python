import torch #type: ignore
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch.optim as optim
import cv2 
import platform
import os
from threading import Event

#python3 -m venv pyenv --system-site-packages
#source pyenv/bin/activate
#pip3 install torch 
#pip3 install torchvision

nn = torch.nn

class IA:
    NB_CLASSES = 2 
    LEARNING_RATE = 0.001
    BATCH_SIZE = 32
    NUM_EPOCHS = 10
    
    def __init__(self, chemin_sauv_model, entrainement = False):
        print("init ia")
        self.__chemin_model = chemin_sauv_model
        if entrainement:
            self.__model = nn.Sequential(
                nn.Conv2d(3, 16, 3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(2),
                nn.Conv2d(16, 32, 3, padding=1),
                nn.ReLU(),
                nn.MaxPool2d(2),
                nn.Flatten(),
                nn.Linear(32 * 32 * 32, 128),
                nn.ReLU(),
                nn.Linear(128, self.NB_CLASSES)
            )
        else:
            self.__model = torch.load(chemin_sauv_model, weights_only=False)
    
    def entrainer(self, dossier_train):
        print("dossier train:", dossier_train)
        transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
        ])
        train = datasets.ImageFolder(os.path.join(dossier_train), transform=transform)
        train_loader = DataLoader(train, self.BATCH_SIZE, shuffle=True)        
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        criterion = nn.CrossEntropyLoss()					# Fonction de coût
        optimizer = optim.Adam(self.__model.parameters(), lr=self.LEARNING_RATE)		# Descente de gradient
        
        self.__model.to(self.__device)
        self.__model.train()
        
        for epoch in range(self.NUM_EPOCHS):
            total_loss, correct = 0, 0
            for images, labels in train_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = self.__model(images)
                loss = criterion(outputs, labels)
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
                correct += (outputs.argmax(1) == labels).sum().item() # Nombre de prédictions correctes dans un batch  
                acc = 100 * correct / len(train_loader.dataset)
            print(f"Epoch {epoch+1}, Loss: {total_loss:.4f}, Accuracy: {acc:.2f}%")
        
        torch.save(self.__model, self.__chemin_model)

    def evaluer(self, dossier_eval):
        print("dossier eval:", dossier_eval)
        transform = transforms.Compose([
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
        ])
        eval = datasets.ImageFolder(os.path.join(dossier_eval), transform=transform)
        eval_loader = DataLoader(eval, self.BATCH_SIZE, shuffle=True)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self.__model.eval()	# mode évaluation
        correct = 0
        with torch.no_grad():	# économise temps et mémoire
            for images, labels in eval_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = self.__model(images)
                correct += (outputs.argmax(1) == labels).sum().item() 
                acc = 100 * correct / len(eval_loader.dataset) 
                print(f"Accuracy: {acc:.2f}%")

    def analyser(self, img):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.__model.eval()
        labels = ["obstacle", "voie_libre"] # en ordre alphabétique
        # Prétraitement de l’image
        frame_resized = cv2.resize(img, (128, 128))
        image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB) # Peut-être pas nécessaire
        # Permutation des axes Hauteur, Largeur, Canal en CHL 
        # Unsqueeze ajoute une dimension pour le numéro du batch (batch, C, H, L)
        image = torch.tensor(image.transpose(2, 0, 1)).float().unsqueeze(0) / 255.0
        image = image.to(device)
        with torch.no_grad():
            output = self.__model(image)
            _, predicted = torch.max(output, 1) # max de la dimension 1
            label = labels[predicted.item()] if predicted.item() < len(labels) else "?"
            print("output: ", output,"|label: ", label)
            return label;

        