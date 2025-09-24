from gab_robot import Robot
import numpy as np  # type: ignore
import cv2  # type: ignore
import threading
import time
from dictKeyValue import MapTouches

DIST_MIN = 1  #m

#initialisation du robot
robot = Robot(True, True)

#initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)

maycontinue = True #bool, permet d'arrêter le programme proprement
#del verte = sonar droit
#del jaune = sonar gauche

while maycontinue: #tant qu'on peut continuer
    img = np.zeros((512, 512, 3), np.uint8) #set limage de fond pour l'écran de oCV
    
    
    #set le texte pour la fenetre oCV
    cv2.imshow("Labo 2", img) #montrer la fenêtre de openCV

    key = cv2.waitKeyEx(30)
    
    if key == -1:
        continue
    else:
        key = str(key.to_bytes(), "utf-8")

    if key == "x":
        maycontinue = False

    mapper.map(key) 

robot.shutdown()
