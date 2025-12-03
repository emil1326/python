import time
from rn import RadioNavigation
from gab_robot import Robot
from labs_ses2.orientation import Orientation
import numpy as np
import cv2
from dictKeyValue import MapTouches

IN1 = 5
IN2 = 6
ENA = 13

IN3 = 15
IN4 = 14
ENB = 18

HAUTEUR = 480
LARGEUR = 480

TARGET_OBJET = np.array([100.0, 100.0])  # position de l'objet à atteindre
TARGET_DROPOFF = np.array([120.0, 120.0])  # position où lâcher l'objet

# create orientation (IMU) and pass it to the Robot for closed-loop turns
orientation = Orientation()
robot = Robot(IN1, IN2, ENA, IN3, IN4, ENB, orientation=orientation)
rn = RadioNavigation()

# initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)

img = np.zeros((HAUTEUR, LARGEUR, 3), np.uint8)

may_continue = rn.demarrer()

while may_continue:
    # 1. obtenir la position du robot
    posDebut = rn.get_position()

    # get angle

    robot.avancer(0.5)
    time.sleep(1)

    newpos = rn.get_position()

    robot.arreter()

    diffpos = newpos - posDebut

    # determine current heading from the measured forward displacement
    if np.linalg.norm(diffpos) < 1e-6:
        print("Déplacement trop petit pour déterminer l'orientation (ignore)")
        continue

    # use IMU magnetometer heading (degrees) as current heading if available
    # orientation.mag_heading is in degrees (see `labs_ses2/orientation.py`)
    current_heading_deg = float(orientation.mag_heading)
    current_heading = np.radians(current_heading_deg)

    # compute heading to the target object from the current position
    to_target = TARGET_OBJET - newpos
    if np.linalg.norm(to_target) < 1e-6:
        print("Déjà sur la cible")
        continue

    target_heading = np.arctan2(to_target[1], to_target[0])
    target_heading_deg = np.degrees(target_heading)

    # signed smallest angle difference in [-pi, pi]
    def wrap_to_pi(a: float) -> float:
        return (a + np.pi) % (2 * np.pi) - np.pi

    # angle error using IMU heading (degrees), wrapped to [-180, 180]
    def wrap_to_180(a_deg: float) -> float:
        return (a_deg + 180.0) % 360.0 - 180.0

    angle_err_deg = wrap_to_180(target_heading_deg - current_heading_deg)
    print(f"Angle erreur (deg): {angle_err_deg:.1f}")

    # Closed-loop turning using IMU heading feedback
    TURN_SPEED = 0.65  # motor speed for turning (0..1) — tune as needed
    ANGLE_THRESHOLD_DEG = 5.0  # stop turning when within this tolerance
    POLL_DT = 0.05  # s
    TIMEOUT = 5.0  # s max to avoid infinite loops

    start_time = time.perf_counter()
    # decide initial direction
    if abs(angle_err_deg) > ANGLE_THRESHOLD_DEG:
        if angle_err_deg > 0:
            robot.tourner_gauche(TURN_SPEED)
        else:
            robot.tourner_droite(TURN_SPEED)

        while True:
            # read updated heading from IMU
            current_heading_deg = float(orientation.mag_heading)
            angle_err_deg = wrap_to_180(target_heading_deg - current_heading_deg)
            if abs(angle_err_deg) <= ANGLE_THRESHOLD_DEG:
                break
            if (time.perf_counter() - start_time) > TIMEOUT:
                print("Turn timeout — stopping")
                break
            time.sleep(POLL_DT)

        robot.arreter()

    # goto target
    
    robot.avancer(0.5)
    time.sleep(1)

    # 3. rendu proche

    # use camera 
    
    

    cv2.imshow("PFI", img)
    # attendre une touche
    key = cv2.waitKeyEx(30)

    # gestion d'erreur
    if key == -1 or key > 255:
        continue

    t = chr(key)
    # si on demande d'arrêter
    if t == "x":
        maycontinue = False  # mettre le flag de la boucle a False pour l'arrêter
        print("arrêt")
    # mapper pour appeler les bonnes fonctions selon la touche appuyée
    mapper.map(t)
