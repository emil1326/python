#Gabriel Pereira Levesque
#Laboratoire IV

from gab_robot import Robot
import numpy as np  # type: ignore
import cv2  # type: ignore
import threading
import time
from dictKeyValue import MapTouches

DIST_MIN = 1  #m

#initialisation du robot
robot = Robot(False, False)

#initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)

maycontinue = True #bool, permet d'arrêter le programme proprement

img = np.zeros((512, 512, 3), np.uint8) #set limage de fond pour l'écran de oCV

while maycontinue: #tant qu'on peut continuer
   
    #routine pseudo code
    #1. capturer une image
    #2. convertir l'image en hsv
    #3. binariser l'image hsv 
    #4. filtrer l'image binarisé pour avoir le blob de la balle
    #5. detecter quelle action faire selon les coordonnees du centre du blob    
    #6. dessiner le rectangle autour du blob     
    
    #set le texte pour la fenetre oCV
    cv2.imshow("Labo 4", img) #montrer la fenêtre de openCV

    key = cv2.waitKeyEx(30) #attendre 30ms pour l'appui d'une touche 
    
    #gestion d'erreur 
    if key == -1 or key > 255:
        continue

    t = chr(key)
    #si on demande d'arrêter
    if t == "x":
        maycontinue = False #mettre le flag de la boucle a False pour l'arrêter
    #mapper pour appeler les bonnes fonctions selon la touche appuyée
    mapper.map(t) 
