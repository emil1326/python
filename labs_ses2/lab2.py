#Gabriel Pereira Leves et Emilien
#Laboratoire II | 15 septembre 2025

from sonar import Sonar
from dels import Dels
import numpy as np  # type: ignore
import cv2  # type: ignore
import threading
import time
from basicPortControlSystemGPIO import basicPortControlSystemGPIO as PCS

from dictKeyValue import MapTouches

delJaune = PCS(20)
delRouge = PCS(20)

delJaune.changeState(1)

mapper = MapTouches()

maycontinue = True

sonarG = Sonar(25, 8)  # sonar de gauche
sonarD = Sonar(20, 21)  # sonar de droite


def triggerSonar():
    while maycontinue:
        sonarD.trigger()
        time.sleep(0.1)


triggerThread = threading.Thread(target=triggerSonar)
triggerThread.start()

while maycontinue:

    img = np.zeros((512, 512, 3), np.uint8)
    cv2.imshow("Labo 1", img)

    key = cv2.waitKeyEx(1)

    if ord(key) == "x":
        maycontinue = False

    key = cv2.waitKeyEx(30)  # 30 millisecondes

    mapper.map(ord(key))
    time.sleep(0.5)

triggerThread.join()
