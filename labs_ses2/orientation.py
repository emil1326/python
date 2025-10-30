from ast import main
import threading
import time


class orientation:
    # mainThread = None
    waitTime = 50  # ms

    class orientationData:
        def __init__(self, ax=0, ay=0, az=0, gx=0, gy=0, gz=0, mx=0, my=0, mz=0):
            self.ax = ax
            self.ay = ay
            self.az = az
            self.gx = gx
            self.gy = gy
            self.gz = gz
            self.mx = mx
            self.my = my
            self.mz = mz

    def __init__(self):
        self.mainThread = None  # main thread of orientation
        self.calibrationDone = False  # indicates if calibration has been done
        self.calibrating = False  # indicates if calibration is in progress
        self.estImmobile = False  # indicates if the device is immobile

        # offset values for calibration (ax, ay, az, gx, gy, gz, mx, my, mz)
        self.angleOffset = orientation.orientationData(0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.currentAngle = orientation.orientationData(0, 0, 0, 0, 0, 0, 0, 0, 0)

        self.mainThread = threading.Thread(target=self.mainLoop)
        self.mainThread.start()

    def mainLoop(self):
        while True:
            if self.calibrating:
                # Calibration logic here
                pass
            else:
                # Normal operation logic here
                pass
            time.sleep(self.waitTime / 1000.0)

    def startCalibration(self):
        self.calibrating = True
        # Calibration logic here

        # while on do 8 figures on peut get tout le data i think?

        # end of calibration
        self.calibrating = False
        self.calibrationDone = True
