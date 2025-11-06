# Gabriel Pereira Levesque & Émilien Devauchelle
# Laboratoire VI | 27 octobre 2025

import time
from orientation import Orientation
from pprint import pformat

# initialisations
orientation = Orientation(mag_cal_seconds=5, gx_window_size=50)

mayContinue = True  # bool, permet d'arrêter le programme proprement

while mayContinue:  # tant qu'on peut continuer
    if orientation.calibrating.is_set():
        print("Calibrating magnetometer... Please keep the robot still.")
        time.sleep(1)
        continue

    print(
        f"Yaw: {orientation.yaw:.2f} rad, Mag Heading: {orientation.mag_heading:.2f} rad"
    )
    raw = orientation._read_imu()
    print("Raw data:\n" + pformat(vars(raw), indent=2))

    key = cv2.waitKeyEx(30)  # attendre 30ms pour l'appui d'une touche

    # gestion d'erreur
    if key == -1 or key > 255:
        continue

    t = chr(key)
    # si on demande d'arrêter
    if t == "x":
        maycontinue = False  # mettre le flag de la boucle a False pour l'arrêter
        print("arrêt")
