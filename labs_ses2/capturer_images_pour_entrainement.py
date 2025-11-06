from camera import Camera
from gab_robot import Robot
from dictKeyValue import MapTouches
import cv2 # type: ignore
import time


# initialisation du robot
robot = Robot()
camera = Camera()

# initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)

maycontinue = True
compteur = 0
dossier_mere_images = "dataset"

while maycontinue:

    img = camera.capturer_image_bgr()
    
    cv2.putText(
        img, "o: obstacle", (0, camera.HAUTEUR,), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 50, 50), 2
    )
    cv2.putText(
        img, "l: voie libre", (0, camera.HAUTEUR - 30), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (50, 255, 50), 2
    )
    
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

    
    camera.sauvegarder_image_ml(dossier_mere_images, img, key, time.time())
    mapper.map(key)
