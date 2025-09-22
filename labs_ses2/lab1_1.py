from datetime import datetime
import time
from gab_robot import Robot
import numpy as np  # type: ignore
import cv2  # type: ignore

from dictKeyValue import MapTouches

#initialisation du robot
robot = Robot(True, True)

#initialisation du mapper qui associe les touches à des actions
mapper = MapTouches(robot)

maycontinue = True

while maycontinue:

    img = np.zeros((512, 512, 3), np.uint8)
    cv2.imshow("Labo 1", img)

    key = cv2.waitKeyEx(1)

    if key == -1:
        continue
    else:
        key = str(key.to_bytes(), "utf-8")

    print("curr :", key)

    if key == "x":
        maycontinue = False

    mapper.map(key)

    time.sleep(0.05)
