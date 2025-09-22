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

#initialiser et partir le thread
triggerThread = threading.Thread(target=robot.trigger_sonar_d)
delsThread = threading.Thread(target=robot.clignoter_dels) 
triggerThread.start()
delsThread.start()

while maycontinue: #tant qu'on peut continuer
    img = np.zeros((512, 512, 3), np.uint8) #set limage de fond pour l'écran de oCV
    distance = robot.get_distance('d')
    text = f"distance: {distance} m"
    
    if distance > DIST_MIN and delsThread.is_alive():
        robot.arreter_clignoter_dels()
    elif not Robot.dels_clignotent:
        robot.clignoter_dels()
    
    #set le texte pour la fenetre oCV
    cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (200, 150, 255), 2)
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

triggerThread.join()
delsThread.join()
