# Gabriel Pereira Levesque & Émilien Devauchelle
# Laboratoire VII | 17 novembre 2025

from camera import Camera;
from ia import IA;
from gab_robot import Robot;
from dictKeyValue import MapTouches;
from os import path
import cv2

robot = Robot()
camera = Camera()
ia = IA(path.join("ia_model", "gab_ai.pt"))

# initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)

maycontinue = True
print("entre dans la main boucle")

pt1 = (camera.LARGEUR-32, 0)
pt2 = (camera.LARGEUR, 32)
voie_libre_color = (0,255,0)
obstacle_color = (0,0,255)

while maycontinue:
    img = camera.capturer_image_bgr()
    
    label = ia.analyser(img)
    
    voie_libre = label=="voie_libre"
    
    if not voie_libre:
        robot.arreter()
    
    cv2.rectangle(img, pt1, pt2, voie_libre_color if voie_libre else obstacle_color, -1)    
    cv2.imshow("Labo 7", img)

    key = cv2.waitKeyEx(30)

    if key == -1:
        continue
    else:
        key = str(key.to_bytes(), "utf-8")

    print("curr :", key)

    if key == "x":
        maycontinue = False

    mapper.map(key, label=="voie_libre")

