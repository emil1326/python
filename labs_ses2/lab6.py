# Gabriel Pereira Levesque & Émilien Devauchelle
# Laboratoire V | 27 octobre 2025

import time
from orientation import Orientation
from pprint import pformat

# initialisations
orientation = Orientation(mag_cal_seconds=5, gx_window_size=50)

mayContinue = True  # bool, permet d'arrêter le programme proprement

while mayContinue:  # tant qu'on peut continuer
    if orientation.calibrating:
        print("Calibrating magnetometer... Please keep the robot still.")
        time.sleep(1)
        continue

    print(
        f"Yaw: {orientation.yaw:.2f} rad, Mag Heading: {orientation.mag_heading:.2f} rad"
    )
    raw = orientation._read_imu()
    print("Raw data:\n" + pformat(raw, indent=2))

    time.sleep(0.1)
