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

#initialisation du mapper qui associe les touches à des actions du robot
mapper = MapTouches(robot)

maycontinue = True #bool, permet d'arrêter le programme proprement

#partir les sonars
robot.trigger_sonars()

#del verte = sonar droit
#del jaune = sonar gauche

while maycontinue: #tant qu'on peut continuer
    img = np.zeros((512, 512, 3), np.uint8) #set limage de fond pour l'écran de oCV
    #distances detectées par les sonars
    distance_d = robot.get_distance('d') #sonar de droite
    distance_g = robot.get_distance('g') #sonar de gauche
    
    #s'il n'y a pas de distance détectée
    if distance_d is None:
        distance_d = -1 #envoi d'une distance anormale
    if distance_g is None:
        distance_g = -1    #''
    
    #si la distance du sonar de droite est plus grande que la distance minimum
    if distance_d > DIST_MIN:
        robot.arreter_clignoter_del_verte() #on arrete de faire clignoter la del vert
    else: #si la distance est plus petite ou égale au minimum
        robot.clignoter_del_verte(distance_d) #on fait clignoter la del verte. La vitesse de clignotement (sleep) est controlée par la distance (+ petite = + vite)
    #même chose pour la distance détectée par le sonar de gauche
    if distance_g > DIST_MIN: 
        robot.arreter_clignoter_del_jaune()
    else:
        robot.clignoter_del_jaune(distance_g)
    
    
    #set le texte pour la fenetre oCV
    text_dist_g = f"distance gauche: {distance_g:.2f}m" #texte de pour distance du sonar de gauche
    text_dist_d = f"distance droite: {distance_d:.2f}m" #texte de pour distance du sonar de droite
    #mettre les texte un par dessus l'autre (\n ne fonctionne pas)
    cv2.putText(img, text_dist_g, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (200, 150, 255), 2) 
    cv2.putText(img, text_dist_d, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (200, 150, 255), 2)
    #montrer la fenêtre de openCV
    cv2.imshow("Labo 2", img) 

    key = cv2.waitKeyEx(30) #attendre 30ms pour l'appui d'une touche 
    
    #gestion d'erreur 
    if key == -1:
        continue
    else:
        key = chr(key)
        
    #si on demande d'arrêter
    if key == "x":
        maycontinue = False #mettre le flag de la boucle a False pour l'arrêter
    #mapper pour appeler les bonnes fonctions selon la touche appuyée
    mapper.map(key) 
