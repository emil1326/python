# Gabriel Pereira Levesque
# Laboratoire V | 27 octobre 2025
#from robot import Robot
from camera import Camera
import cv2  # type: ignore

# initialisations
camera = Camera()

choix = input('Voulez-vous créer un modèle (c) ou en détecter un (enter)? ')

if(choix == 'c'):
    fichier = input("tappez le nom du fichier dans lequel sauvegarder l'image: ")
    camera.creation_du_model('c', fichier)
else:
    nom_model = input("tappez le nom du fichier dans lequel se trouve le modèle a détecter: ")
    nom_masque = nom_model.replace("model", "masque")
    print("nom masque: ", nom_masque)
    camera.rechercher_model(nom_model, nom_masque)

cv2.destroyAllWindows()
