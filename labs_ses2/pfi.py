from rn import RadioNavigation
from gab_robot import Robot
import numpy as np
import cv2
from dictKeyValue import MapTouches

IN1 = 5
IN2 = 6
ENA = 13

IN3 = 15
IN4 = 14
ENB = 18

HAUTEUR = 480
LARGEUR = 480

robot = Robot(IN1, IN2, ENA, IN3, IN4, ENB)
rn = RadioNavigation()

# initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)

img = np.zeros((HAUTEUR, LARGEUR, 3), np.uint8)

may_continue = rn.demarrer()

while may_continue:
    #1. obtenir la position du robot
    rn.get_position() 
         
    #2. diriger vers pos objet
    
    #3. rendu proche 
    
    
    cv2.imshow("PFI", img)
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