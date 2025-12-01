# Laboratoire I version du 22 septembre 2025
# Par Gabriel Pereira Levesque et Émilien

from datetime import datetime
import time
from gab_robot import Robot
from gab_orientation import Orientation
import numpy as np  # type: ignore
import cv2  # type: ignore

from dictKeyValue import MapTouches

#fix: inversé IN1 (14) et IN2 (15)
IN1 = 15
IN2 = 14
ENA = 18
#fix: inversé IN3 (5) et IN4 (6)
IN3 = 6
IN4 = 5
ENB = 13

# initialisations
orientation = Orientation()
robot = Robot(IN1, IN2, ENA, IN3, IN4, ENB, orientation=orientation)

# initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)


maycontinue = orientation.demarrer(robot)

img = np.zeros((512, 512, 3), np.uint8)

while maycontinue:
    cv2.imshow("Labo 6", img)       

    #attendre une touche
    key = cv2.waitKeyEx(30)

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