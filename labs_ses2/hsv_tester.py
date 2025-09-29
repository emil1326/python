# Modifié par J. S. Morales
# 21 septembre 2025

import cv2 # type: ignore
from picamera2 import Picamera2, Preview # type: ignore
import numpy as np # type: ignore

def track_bar_cb(x):
    pass

LARGEUR = 640
HAUTEUR = 480

picam2 = Picamera2()

config = picam2.create_preview_configuration(main={"format": 'RGB888', 
                                             "size": (LARGEUR, HAUTEUR)})
picam2.align_configuration(config)
(largeur_img, hauteur_img) = config["main"]["size"]
picam2.configure(config)
picam2.start()

#cap = cv2.VideoCapture(0)


titre_fenetre = "HSV Tester"
cv2.namedWindow(titre_fenetre)
cv2.createTrackbar('Teinte min',  titre_fenetre, 0, 179, track_bar_cb)
cv2.createTrackbar('Teinte max', titre_fenetre, 0, 179, track_bar_cb)
cv2.createTrackbar('Saturation min', titre_fenetre, 0,255, track_bar_cb)
cv2.createTrackbar('Saturation max', titre_fenetre, 0,255, track_bar_cb)
cv2.createTrackbar('Valeur min', titre_fenetre, 0, 255, track_bar_cb)
cv2.createTrackbar('Valeur max', titre_fenetre, 0, 255, track_bar_cb)

print(f"Pour quitter presser la touche 'q'.")

terminer = False
while not terminer:

    min_teinte = cv2.getTrackbarPos('Teinte min', titre_fenetre)
    max_teinte = cv2.getTrackbarPos('Teinte max', titre_fenetre)
    sat_min = cv2.getTrackbarPos('Saturation min', titre_fenetre)
    sat_max = cv2.getTrackbarPos('Saturation max', titre_fenetre)
    val_min = cv2.getTrackbarPos('Valeur min', titre_fenetre)
    val_max = cv2.getTrackbarPos('Valeur max', titre_fenetre)

    teinte_min = np.array([min_teinte, sat_min, val_min])
    teinte_max = np.array([max_teinte, sat_max, val_max])

    print(f"{teinte_min}, {teinte_max}")
    frame_bgr = picam2.capture_array()
    """ ret, frame_bgr = cap.read()
    if not ret:
        break """
    
    frame_hsv = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2HSV)
    frame_disc = cv2.inRange(frame_hsv, teinte_min, teinte_max)
    cv2.imshow("Image BGR", frame_bgr)
    cv2.imshow("HSV", frame_hsv)
    cv2.imshow("Image disc", frame_disc)

    choix = cv2.waitKey(30)
    if  choix == ord('q'):
        terminer = True    

cv2.destroyAllWindows()


