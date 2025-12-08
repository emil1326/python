#Gabriel Pereira Levesque 
#Laboratoire VIII

from gab_robot import Robot
from gab_lidar import (Lidar, Models)
import numpy as np  # type: ignore
import cv2  # type: ignore


from dictKeyValue import MapTouches

LARGEUR = 480
HAUTEUR = 480
PORT_LIDAR = "/dev/ttyUSB0"
MODEL = Models.X4 # a changer selon le model quon tombe dessus

# initialisation du robot

#fix: inversé IN1 (14) et IN2 (15)
IN1 = 5
IN2 = 6
ENA = 13
#fix: inversé IN3 (5) et IN4 (6)
IN3 = 15
IN4 = 14
ENB = 18

robot = Robot(IN1, IN2, ENA, IN3, IN4, ENB)
lidar = Lidar(PORT_LIDAR, MODEL)

# initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)

img = np.zeros((HAUTEUR, LARGEUR, 3), np.uint8)

#comme demarrer retourne un bool (True si reussite | False si echec)
maycontinue = lidar.demarrer() #part la boucle seulement si demarrer a fonctionné
print('maycontinue: ', maycontinue)

while maycontinue:    
    points = lidar.getPointsObstacle()
    #dessiner sur limage (passée par reférence)
    lidar.dessinerSurImage(img, LARGEUR, HAUTEUR)
    
    if(points is not None):
        for (x, y) in points:
            if(lidar.obstacleEnAvant(x, y)):
                print('!!! obstacle en AVANT !!!')
            if(lidar.obstacleDroite(x, y)):
                print('!!! obstacle a DROITE !!!')
            if(lidar.obstacleGauche(x,y)):
                print('!!! obstacle a GAUCHE !!!')
            
    
    #montrer notre beau travail
    cv2.imshow("Test lidar", img)
    
    #réinitialisation de l'image pour un frame par fram
    img[:] = 0
    
    #attendre une touche
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

#nettoyer le robot de tout ces processus
cv2.destroyAllWindows()
lidar.arreter()
