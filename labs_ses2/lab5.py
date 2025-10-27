# Gabriel Pereira Levesque & Émilien
# Laboratoire V | ??DATE??
#from robot import Robot
from camera import Camera
import numpy as np  # type: ignore
import cv2  # type: ignore
import threading
import time
from dictKeyValue import MapTouches

# initialisations
#robot = Robot()
camera = Camera()

# initialisation du mapper qui associe les touches à des actions
mapper = MapTouches()

maycontinue = True  # bool, permet d'arrêter le programme proprement

choix = input('Voulez-vous créer un modèle (c) ou en détecter un (enter)? ')

if(choix == 'c'):
    fichier = input("tappez le nom du fichier dans lequel sauvegarder l'image: ")
    camera.creation_du_model('c', fichier)
else:
    nom_model = input("tappez le nom du fichier dans lequel se trouve le modèle a détecter: ")
    nom_masque = nom_model.replace("model", "masque")
    camera.rechercher_model(nom_model, nom_masque)

cv2.destroyAllWindows()
