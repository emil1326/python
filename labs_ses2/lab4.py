# Gabriel Pereira Levesque
# Laboratoire IV

from gab_robot import Robot
from camera import Camera
import numpy as np  # type: ignore
import cv2  # type: ignore
import threading
import time
from dictKeyValue import MapTouches

DIST_MIN = 1  # m

# initialisation du robot
robot = Robot(False, False)
camera = Camera()

# initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)

maycontinue = True  # bool, permet d'arrêter le programme proprement

img = np.zeros((512, 512, 3), np.uint8)  # set limage de fond pour l'écran de oCV

MIN_AIRE = 100
MAX_AIRE = 3000
FULLMIN_X = 40
MIN_X = 80
FULLMAX_X = 280
MAX_X = 240
VITESSE_AIRE_MIN = MIN_AIRE
VITESSE_AIRE_MAX = MAX_AIRE / 5


def findVitesse(aireCurrente):
    vtemp = aireCurrente * MAX_AIRE / MIN_AIRE

    return aireCurrente / vtemp


while maycontinue:  # tant qu'on peut continuer

    # routine pseudo code
    # 1. capturer une image
    img_bgr = camera.capturer_image_bgr()
    # 2. convertir l'image en hsv
    img_hsv = camera.convertir_image_bgr2hsv(img_bgr)
    # 3. binariser l'image hsv
    img_bin = camera.binariser_image(img_hsv)
    # 4. filtrer l'image binarisé pour avoir le blob de la balle
    contour_balle = camera.get_plus_gros_contour(img_bin, {"min": 0, "max": 240})
    # 5. detecter quelle action faire selon les coordonnees du centre du blob
    aire, centre = camera.get_dimensions_contour(contour_balle)
    if aire <= MIN_AIRE:  # trop loin!
        print("arreter")
        robot.arreter()
    elif aire > MAX_AIRE:  # trop proche!
        print("arreter")
        robot.arreter()
    else:
        if centre["x"] <= FULLMIN_X:
            robot.tourner_gauche()
            print("Full gauche")
        elif centre["x"] <= MIN_X:  # à gauche!
            robot.diagonale_gauche()
            print("gauche")
        elif centre["x"] >= FULLMAX_X:
            robot.tourner_droite()
            print("Full droite")
        elif centre["x"] >= MAX_X:
            robot.diagonale_droite()
            print("droite")
        else:
            robot.avancer(findVitesse(aire))
            print("avancer")
    # 6. dessiner le rectangle autour du blob
    camera.dessiner_rectangle_sur_image(img_bgr, contour_balle)

    # set le texte pour la fenetre oCV
    cv2.imshow("Labo 4", img_bgr)  # montrer la fenêtre de openCV
    cv2.imshow("Labo 4 binarise", img_bin)
    key = cv2.waitKeyEx(30)  # attendre 30ms pour l'appui d'une touche

    # gestion d'erreur
    if key == -1 or key > 255:
        continue

    t = chr(key)
    # si on demande d'arrêter
    if t == "x":
        maycontinue = False  # mettre le flag de la boucle a False pour l'arrêter
        print('arrêt')
    # mapper pour appeler les bonnes fonctions selon la touche appuyée
    mapper.map(t)

cv2.destroyAllWindows()
