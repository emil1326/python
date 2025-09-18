#Gabriel Pereira Levesque et Emilien
#Laboratoire II | 15 septembre 2025

from sonar import Sonar
import numpy as np  # type: ignore
import cv2  # type: ignore
import threading
import time
from dictKeyValue import MapTouches

DIST_MIN = 1  #m

#initialisation du mapper qui associe les touches à des actions
mapper = MapTouches()

maycontinue = True #bool, permet d'arrêter le programme proprement

#initialisation des sonars
sonarG = Sonar(25, 8)  # sonar de gauche
sonarD = Sonar(20, 21)  # sonar de droite

dels = Dels()

#fonction pour le thread
def triggerSonar():
    while maycontinue:
        sonarD.trigger() #appel trigger
        time.sleep(0.1) #10x par seconde


#initialiser et partir le thread
triggerThread = threading.Thread(target=triggerSonar)
triggerThread.start() 

img = np.zeros((512, 512, 3), np.uint8) #set limage de fond pour l'écran de oCV

while maycontinue: #tant qu'on peut continuer
    distance = sonarD.get_distance()
    text = f"distance: {distance} m"
    
    if distance > DIST_MIN:
            dels.eteindre()
    else:
        dels.clignoter_jaune()
        dels.clignoter_verte()           
     
    #set le texte pour la fenetre oCV
    cv2.putText(img, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (200, 150, 255), 2)
    cv2.imshow("Labo 2", img) #montrer la fenêtre de openCV

    key = cv2.waitKeyEx(30)  #attend pour un touche pendant 30 millisecondes

    if ord(key) == "x": #si cest x on ferme le programme proprement
        maycontinue = False   

    mapper.map(ord(key)) #map la touche
    
    time.sleep(0.5) #sleep pour pas saturer le CPU
    

triggerThread.join()
