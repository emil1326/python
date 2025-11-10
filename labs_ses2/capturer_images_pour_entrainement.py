from camera import Camera
from gab_robot import Robot
from dictKeyValue import MapTouches
import cv2 # type: ignore
import time
import os


# initialisation du robot
robot = Robot()
camera = Camera()

# initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)

maycontinue = True
compteur_voie_libre = 0
compteur_obstacle = 0
dossier_mere_images = "dataset"
dossier_libre = os.path.join(dossier_mere_images, "train", "voie_libre")
dossier_obstacle = os.path.join(dossier_mere_images, "train", "obstacle")
if not os.path.exists(dossier_libre):
    compteur_voie_libre = 0
else:
    compteur_voie_libre = len([f for f in os.listdir(dossier_libre) if f.endswith(".png")])

if not os.path.exists(dossier_obstacle):
    compteur_obstacle = 0
else:
    compteur_obstacle = len([f for f in os.listdir(dossier_obstacle) if f.endswith(".png")])

while maycontinue:

    img = camera.capturer_image_bgr()
    
    cv2.imshow("Capt. img apprentissage", img)

    key = cv2.waitKeyEx(1)

    if key == -1:
        continue
    else:
        key = str(key.to_bytes(), "utf-8")

    print("curr :", key)

    if key == "x":
        maycontinue = False
        cv2.destroyAllWindows()    
    
    camera.sauvegarder_image_ml(dossier_mere_images, img, key, time.time_ns())
    if(key == "o"):
        compteur_obstacle += 1
        print("obstacles: ", compteur_obstacle)
    elif(key == "l"):
        compteur_voie_libre += 1
        print("voie_libre: ", compteur_voie_libre)
        
    mapper.map(key)
