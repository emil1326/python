#Gabriel Pereira Levesque et Emilien
#Laboratoire II | 15 septembre 2025
from dels import Dels
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
maycontinueDels = False

#fonction pour le thread
def triggerSonar():
    while maycontinue:
        sonarD.trigger() #appel trigger
        time.sleep(0.1) #10x par seconde


#initialiser et partir le thread
triggerThread = threading.Thread(target=triggerSonar)
delsThread = threading.Thread(target=clignoterDels) 
triggerThread.start() 
delsThread.start()

img = np.zeros((512, 512, 3), np.uint8) #set limage de fond pour l'écran de oCV

while maycontinue: #tant qu'on peut continuer
    distance = sonarD.get_distance()
    text = f"distance: {distance} m"
    
    if distance > DIST_MIN and delsThread.is_alive():
        maycontinueDels = False
    else:
        maycontinueDels = True
    
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
        maycontinue = False

    mapper.map(key)    

triggerThread.join()
delsThread.join()
