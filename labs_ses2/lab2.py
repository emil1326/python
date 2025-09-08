from sonar import Sonar;
import numpy as np  # type: ignore
import cv2
import threading
import time

from dictKeyValue import MapTouches

mapper = MapTouches()

maycontinue = True

sonarG = Sonar._init(Sonar, 25, 8) #sonar de gauche
sonarD = Sonar._init(Sonar, 20, 21)#sonar de droite

#initialisation des callbacks des DigitalInputDevice
sonarG.echo.when_activated = sonarG.when_activated
sonarG.echo.when_deactivated = sonarG.when_deactivated

sonarD.echo.when_activated = sonarD.when_activated
sonarD.echo.when_deactivated = sonarD.when_deactivated

def triggerSonar():
    while(maycontinue):
        sonarD.trigger.on()
        sonarG.trigger.on()
        time.sleep(0.01)
        sonarD.trigger.off()
        sonarG.trigger.off()
    

triggerThread =  threading.Thread(target=triggerSonar)

while maycontinue:

    img = np.zeros((512, 512, 3), np.uint8)
    cv2.imshow("Labo 1", img)

    key = cv2.waitKeyEx(1)
    
    if ord(key) == "x":
        maycontinue = False

    key = cv2.waitKeyEx(30)  # 30 millisecondes

    mapper.map(ord(key))
