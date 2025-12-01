# Gabriel Pereira Levesque & Émilien Devauchelle
# Laboratoire VI | 27 octobre 2025

import time
from gab_robot import Robot
from orientation import Orientation
from dictKeyValue import MapTouches
from pprint import pformat
import math
import cv2  # type: ignore

print("PreProg lab6")

# initialisations
orientation = Orientation(mag_cal_seconds=5, gx_window_size=50)

# fix: inversé IN1 (14) et IN2 (15)
IN1 = 5
IN2 = 6
ENA = 13
# fix: inversé IN3 (5) et IN4 (6)
IN3 = 15
IN4 = 14
ENB = 18

voiture = Robot(IN1, IN2, ENA, IN3, IN4, ENB, orientation=orientation)
mapper = MapTouches(voiture)

mayContinue = True  # bool, permet d'arrêter le programme proprement

while orientation.calibrating.is_set():
    voiture.tourner_droite()
    print("Calibrage du magnetometre... Gardez le robot en place.")
    time.sleep(1)

voiture.arreter()
print("Calibration complete. Starting main loop. orientation", orientation.mag_heading)
time.sleep(1)

target_tol = 5
max_seconds = 30.0
vitesse_robot = 0.75
min_angle = 358
max_angle = 10
start_time = time.time()
wait_time = orientation.waitTime/1000 

print('wait_time', wait_time)

# tourner jusqu'à ce que l'angle magnétique soit proche de 0 (nord)
while True:
    heading = orientation.mag_heading
    print("orientation ", heading, " degrés")
    if heading > min_angle or heading < max_angle:
        print("Robot aligné vers le nord magnétique.")
        break

    # si heading > 0 on veut le diminuer, donc tourner à droite ;
    # si heading < 0 on veut l'augmenter, donc tourner à gauche.
    if heading > 0 + target_tol:
        voiture.tourner_droite(vitesse_robot)
    else:
        voiture.tourner_gauche(vitesse_robot)

    # sécurité : timeout pour éviter boucle infinie
    if time.time() - start_time > max_seconds:
        print("Timeout pendant l'alignement magnétique.")
        break
    
    time.sleep(wait_time)

voiture.arreter()

time.sleep(1)

voiture.tourner_droite(vitesse_robot)
time.sleep(1)

while True:    
    voiture.tourner_droite(vitesse_robot)
    orientation_curr = orientation.mag_heading
    print("orientation ", orientation_curr, " degrés")
    if orientation_curr > min_angle or orientation_curr < max_angle:
        break
    time.sleep(wait_time)

voiture.arreter()
print("Robot a fait un tour.")
time.sleep(1)

while mayContinue:
    print(
        f"orientations: autour de l'axe des x: {orientation.yaw:.2f} degrés | orientation magnetometre: {orientation.mag_heading:.2f} degrés"
    )

    key = cv2.waitKeyEx(30)  # type: ignore # attendre 30ms pour l'appui d'une touche
    
    time.sleep(5)
    # gestion d'erreur
    if key == -1 or key > 255:
        continue

    t = chr(key)
    # si on demande d'arrêter
    if t == "x":
        maycontinue = False  # mettre le flag de la boucle a False pour l'arrêter
        print("arrêt")
    
    mapper.map(t)
    
