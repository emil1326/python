# Gabriel Pereira Levesque & Émilien Devauchelle
# Laboratoire VII | 17 novembre 2025

from camera import Camera;
from ia import IA;
from gab_robot import Robot;
from dictKeyValue import MapTouches;

robot = Robot()
camera = Camera()
ia = IA()

# initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)

maycontinue = True

while maycontinue:
    img = camera.capturer_image_bgr()
    
    label = ia.analyser(img)
    
    cv2.imshow("Labo 7", img)

    key = cv2.waitKeyEx(1)

    if key == -1:
        continue
    else:
        key = str(key.to_bytes(), "utf-8")

    print("curr :", key)

    if key == "x":
        maycontinue = False

    mapper.map(key, label=="voie_libre")

    time.sleep(0.05)
