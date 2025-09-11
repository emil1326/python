from sonar import Sonar;
import numpy as np  # type: ignore
import cv2 # type: ignore
import threading
import time

from dictKeyValue import MapTouches

mapper = MapTouches()

maycontinue = True

sonarG = Sonar._init(Sonar, 25, 8) #sonar de gauche
sonarD = Sonar._init(Sonar, 20, 21)#sonar de droite

def triggerSonar():
    while(maycontinue):
        sonarD.trigger.on()
        time.sleep(0.05)
        sonarD.trigger.off()
        time.sleep(0.05)
    

triggerThread = threading.Thread(target=triggerSonar)

while maycontinue:

    img = np.zeros((512, 512, 3), np.uint8)
    cv2.imshow("Labo 1", img)

    key = cv2.waitKeyEx(1)
    
    if ord(key) == "x":
        maycontinue = False

    key = cv2.waitKeyEx(30)  # 30 millisecondes

    mapper.map(ord(key))
