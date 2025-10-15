# Gabriel Pereira Levesque & Émilien
# Laboratoire V | ??DATE??

from gab_robot import Robot
from camera import Camera
import numpy as np  # type: ignore
import cv2  # type: ignore
import threading
import time
from dictKeyValue import MapTouches

# initialisation du robot
robot = Robot()
camera = Camera()

# initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)

maycontinue = True  # bool, permet d'arrêter le programme proprement

MODEL = cv2.imread()

while maycontinue:  # tant qu'on peut continuer
    
    key = cv2.waitKeyEx(30)  # attendre 30ms pour l'appui d'une touche

    # gestion d'erreur
    if key == -1 or key > 255:
        continue

    t = chr(key)
    # si on demande d'arrêter
    if t == "x":
        maycontinue = False  # mettre le flag de la boucle a False pour l'arrêter
        print("arrêt")
    # mapper pour appeler les bonnes fonctions selon la touche appuyée
    mapper.map(t)

cv2.destroyAllWindows()
