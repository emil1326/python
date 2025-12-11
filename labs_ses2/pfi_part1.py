# fait par Gabriel

import time
from rn import RadioNavigation
from gab_robot import Robot, ModelsRobot
from orientation import Orientation
import numpy as np  # type: ignore
import cv2  # type: ignore
from dictKeyValue import MapTouches
from camera import Camera
from gab_lidar import Lidar, Models

IN1 = 5
IN2 = 6
ENA = 13

IN3 = 15
IN4 = 14
ENB = 18

HAUTEUR = 480
LARGEUR = 480
PORT_LIDAR = "/dev/ttyUSB0"
MODEL = Models.X4  # a changer selon le model quon tombe dessus

DISTANCE_TRAVEL = 0.50 #m | distance a avancer avant de tourner
distance_avancee = 0.0

NB_POINTS = 4  # checkpoints a atteindre | 4 sommets du rectangle
nb_points_atteints = 0

peut_avancer = True

# constantes utilisées dans la boucle de tournage vers la cible
VITESSE_ROT = 0.7  # vitesse de rotation
ANGLE_TOL = 3.0  # tolérance d'angle au cas ou la lecture est lente
POLL_DT = 0.05  # s | wait time pour ne pas overhead le cpu
TIMEOUT = 5.0  # s | timeout pour éviter une boucle infinie

# initialiser les objets
orientation = Orientation()
robot = Robot(ModelsRobot.lynx, orientation=orientation)
lidar = Lidar(PORT_LIDAR, MODEL)
rn = RadioNavigation()

# initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)

img = np.zeros((HAUTEUR, LARGEUR, 3), np.uint8)

may_continue = rn.demarrer() and lidar.demarrer()

# 1. obtenir la position du robot
posInit = rn.get_position()

while may_continue:
    # verifier pour des obstacles
    points_obstacles = lidar.getPointsObstacle()  # [(x, y), ...]
    if lidar.obstacleEnAvant(points_obstacles):
        print("!!! obstacle en AVANT !!!")
        if peut_avancer:
            robot.reculer()
            time.sleep(0.1)
            robot.arreter()
        peut_avancer = False
        continue
    else:
        peut_avancer = True

    # 2. obtenir la distance avancee jusqua present
    pos_avancee = rn.get_position()
    distance_courante = rn.get_distance(posInit, pos_avancee)
    posInit = pos_avancee
    
    if distance_courante is not None:
        distance_avancee += distance_courante

    # 2.A avancer en ligne droite vers le prochain point juste quand on a une position correcte
    if pos_avancee is not None and peut_avancer:
        robot.avancer() 
    
    #3 si la distance est plus grande ou egale a celle a parcourir
    if distance_avancee >= DISTANCE_TRAVEL:
        print("distance avancee: ", distance_avancee)
        robot.arreter()

        #on incremente le nombre de points atteints
        nb_points_atteints += 1
        distance_avancee = 0
        print("nb points", nb_points_atteints)
        #tourner de 90 degres vers la gauche  
        orientation.turnByYaw(robot, 90)
        
        
    if nb_points_atteints == NB_POINTS:
        print("!!! nb_points atteint")
        may_continue = False  # mettre le flag de la boucle a False pour l'arrêter
    
    cv2.imshow("PFI p.1", img)
    # attendre une touche
    key = cv2.waitKeyEx(30)

    # gestion d'erreur
    if key == -1 or key > 255:
        continue

    t = chr(key)
    # si on demande d'arrêter ou si le robot a effectue sa tache
    
    if t == "x":
        may_continue = False  # mettre le flag de la boucle a False pour l'arrêter
        print("arrêt")
    # mapper pour appeler les bonnes fonctions selon la touche appuyée
    mapper.map(t, peut_avancer)
