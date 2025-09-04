import numpy as np  # type: ignore
import cv2  # type: ignore

from dictKeyValue import MapTouches

mapper = MapTouches()

maycontinue = True

while maycontinue:

    img = np.zeros((512, 512, 3), np.uint8)
    cv2.imshow("Labo 1", img)

    key = cv2.waitKeyEx(1)

    if ord(key) == "x":
        maycontinue = False

    key = cv2.waitKeyEx(30)  # 30 millisecondes

    mapper.map(ord(key))
