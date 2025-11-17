# Gabriel Pereira Levesque & Émilien Devauchelle
# Laboratoire VI | 27 octobre 2025

import time
from gab_robot import Robot
from orientation import Orientation
from dictKeyValue import MapTouches
from pprint import pformat
import cv2  # type: ignore

print("PreProg lab6")

# initialisations
orientation = Orientation(mag_cal_seconds=5, gx_window_size=50)
voiture = Robot(orientation=orientation)
mapper = MapTouches(voiture)

mayContinue = True  # bool, permet d'arrêter le programme proprement

while orientation.calibrating.is_set():
    print("Calibrage du magnetometre... Gardez le robot en place.")
    time.sleep(1)

print("Calibration complete. Starting main loop. orientation", orientation.mag_heading)
time.sleep(1)  

while orientation.mag_heading < 0:
    voiture.tourner_gauche(0.5)
    time.sleep(0.1)
    
voiture.arreter()
print("Robot aligné vers le nord magnétique.")
time.sleep(1)

while orientation.mag_heading > 0.1:
    voiture.tourner_droite(0.5)
    time.sleep(0.1)
    
voiture.arreter()
print("Robot a fait un tour.")
time.sleep(1)

while mayContinue:
    # print(orientation._read_imu().__repr__())

    print(
        f"orientations: autour de l'axe des x: {orientation.yaw:.2f} rad | orientation magnetometre: {orientation.mag_heading:.2f} rad"
    )

    key = cv2.waitKeyEx(30)  # type: ignore # attendre 30ms pour l'appui d'une touche

    # gestion d'erreur
    if key == -1 or key > 255:
        continue

    t = chr(key)
    # si on demande d'arrêter
    if t == "x":
        maycontinue = False  # mettre le flag de la boucle a False pour l'arrêter
        print("arrêt")

    mapper.map(t)
