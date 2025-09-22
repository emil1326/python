#Gabriel Pereira Levesque et Emilien
#Laboratoire II | 22 septembre 2025

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

#partir les sonars
robot.trigger_sonars()

#del verte = sonar droit
#del jaune = sonar gauche

while maycontinue: #tant qu'on peut continuer
    img = np.zeros((512, 512, 3), np.uint8) #set limage de fond pour l'écran de oCV
    distance_d = robot.get_distance('d')
    distance_g = robot.get_distance('g')
    if distance_d is None:
        distance_d = -1
    if distance_g is None:
        distance_g = -1    
    
    if distance_d > DIST_MIN:
        robot.arreter_clignoter_del_verte()
    else:
        robot.clignoter_del_verte()
        
    if distance_g > DIST_MIN:
        robot.arreter_clignoter_del_jaune()
    else:
        robot.clignoter_del_jaune()
    
    
    #set le texte pour la fenetre oCV
    text_dist_g = f"distance gauche: {distance_g:.2f}m"
    text_dist_d = f"distance droite: {distance_d:.2f}m"
    cv2.putText(img, text_dist_g, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (200, 150, 255), 2)
    cv2.putText(img, text_dist_d, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (200, 150, 255), 2)
    cv2.imshow("Labo 2", img) #montrer la fenêtre de openCV

    key = cv2.waitKeyEx(30)
    
    if key == -1:
        continue
    else:
        key = str(key.to_bytes(), "utf-8")

    print("curr :", key)

    if key == "x":
        robot.arreter_sonars()
        robot.arreter_clignoter_dels()
        maycontinue = False

    mapper.map(key) 

robot.shutdown()
