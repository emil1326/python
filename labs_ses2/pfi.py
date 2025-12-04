import time
from rn import RadioNavigation
from gab_robot import Robot
from labs_ses2.orientation import Orientation
import numpy as np
import cv2
from dictKeyValue import MapTouches
from camera import Camera

IN1 = 5
IN2 = 6
ENA = 13

IN3 = 15
IN4 = 14
ENB = 18

HAUTEUR = 480
LARGEUR = 480

TARGET_OBJET = np.array([3.5, 5])  # position de l'objet à atteindre
TARGET_DROPOFF = np.array([0, 0])  # position où lâcher l'objet

# create orientation (IMU) and pass it to the Robot for closed-loop turns
orientation = Orientation()
robot = Robot(IN1, IN2, ENA, IN3, IN4, ENB, orientation=orientation)
rn = RadioNavigation()
camera = Camera()

# initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)

img = np.zeros((HAUTEUR, LARGEUR, 3), np.uint8)

may_continue = rn.demarrer()
sur_la_cible = False

#calibrer le magnétomètre

while may_continue:
    # 1. obtenir la position du robot
    posDebut = rn.get_position()

    #get angle

    #laisser le robot avancer pour savoir dans quelle direction il est 
    robot.avancer(0.5)
    time.sleep(1)
    
    # obtenir la position par après 
    newpos = rn.get_position()

    robot.arreter()

    diffpos = newpos - posDebut

    # determiner l'angle a tourner pour faire face a la cible
    
    if np.linalg.norm(diffpos) < 1e-6:
        print("Déplacement trop petit pour déterminer l'orientation (ignore)")
        continue

    # trouver lorientation courante du robot
    current_heading_deg = float(orientation.mag_heading)
    current_heading = np.radians(current_heading_deg)

    # trouver la distance vers la cible
    to_target = TARGET_OBJET - newpos
    
    #si on est rendu proche (distance a determiner avec tests)
    if np.linalg.norm(to_target) < 1e-6:
        print("sur la cible")
        sur_la_cible = True
        break; 
        
    
    # trouver l'angle relatif au robot de la cible 
    target_heading = np.arctan2(to_target[1], to_target[0])
    target_heading_deg = np.degrees(target_heading)

    # raporter langle a un [-180, 180]
    def wrap_to_180(a_deg: float) -> float:
        return (a_deg + 180.0) % 360.0 - 180.0

    angle_err_deg = wrap_to_180(target_heading_deg - current_heading_deg)
    print(f"Angle erreur: {angle_err_deg:.1f} degrés")

    # Closed-loop turning using IMU heading feedback
    TURN_SPEED = 0.7  # motor speed for turning
    ANGLE_THRESHOLD_DEG = 3.0  # stop turning when within this tolerance
    POLL_DT = 0.05  # s
    TIMEOUT = 5.0  # s max to avoid infinite loops

    #faire tourner le robot
    start_time = time.perf_counter()
    # decide initial direction
    if abs(angle_err_deg) > ANGLE_THRESHOLD_DEG:
        if angle_err_deg > 0:
            robot.tourner_gauche(TURN_SPEED)
        else:
            robot.tourner_droite(TURN_SPEED)

        while True:
            #  lire le heading du robot pour savoir quand arrêter de tourner
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

MIN_OBJ_X = LARGEUR/3
MAX_OBJ_X = LARGEUR - MIN
while sur_la_cible:
    # 3. rendu proche    
    # use camera 
    img = camera.capturer_image_bgr()
    camera.rechercher_model('path_model', 'path_masque')
    position_img_cible = camera.get_derniere_position_objet()
    
    if(position_img_cible['x']<MIN_OBJ_X):
        robot.tourner_droite()
    elif(position_img_cible['x'] > MAX_OBJ_X):
        robot.tourner_gauche()
    else:
        #attraper l'objet
        break

