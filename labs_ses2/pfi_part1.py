import time
from rn import RadioNavigation
from gab_robot import Robot, ModelsRobot
from labs_ses2.orientation import Orientation
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

DISTANCE_TRAVEL = 0.2 #m | distance a avancer avant de tourner
distance_avancee = 0

NB_POINTS = 4 #checkpoints a atteindre | 4 sommets du rectangle
nb_points_atteints = 0

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
    # 2. avancer en ligne droite vers le prochain point
    robot.avancer()
    
    #verifier pour des obstacles
    points_obstacles = lidar.getPointsObstacle()  # [(x, y), ...]
    if(points_obstacles is not None):
        for (x, y) in points_obstacles:
            if lidar.obstacleEnAvant(x, y):
                robot.arreter()

    # 2.B obtenir la distance avancee jusqua present
    posAvancee = rn.get_position()    
    distance_courante = rn.get_distance(posInit, posAvancee)    
    posInit = posAvancee    
    
    #3 si la distance est plus grande ou egale a celle a parcourir
    if distance_courante >= DISTANCE_TRAVEL:
        #on incremente le nombre de points atteints
        nb_points_atteints += 1
        #tourner de 90 degres vers la gauche    
    
    cv2.imshow("PFI p.1", img)
    # attendre une touche
    key = cv2.waitKeyEx(30)

    # gestion d'erreur
    if key == -1 or key > 255:
        continue

    t = chr(key)
    # si on demande d'arrêter ou si le robot a effectue sa tache
    if t == "x" or nb_points_atteints == NB_POINTS:
        maycontinue = False  # mettre le flag de la boucle a False pour l'arrêter
        print("arrêt")
    # mapper pour appeler les bonnes fonctions selon la touche appuyée
    mapper.map(t)
