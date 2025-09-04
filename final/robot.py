import threading
import time
from gpiozero import PWMOutputDevice  # type: ignore
from moteur import Moteur


class Robot:
    # in1, in2, enA, in3, in4, enB
    allowedEnginePort = [6, 5, 13, 15, 14, 18]

    # portAvancer = portReculer = portPuissance = None

    # pForward = 0  # internal puissance back && forth
    # pBackWard = 0

    def __init__(self):
        self.Lengine = Moteur(6, 5, 13)
        self.Rengine = Moteur(15, 14, 18)

        self.mulSpeed = 1
        self.mulSpeedL = 1
        self.mulSpeedR = 1

        self.pForwardL = 0
        self.pBackWardL = 0
        self.pForwardR = 0
        self.pBackWardR = 0

        self.lastTime = time.perf_counter()
        self.rStateThread = None

    def avancer(self, puissance, duration=None, awaitIT=False):
        self.setOnForTime(puissance, False, duration, "both")

        if awaitIT and duration is not None:
            time.sleep(duration)

    def reculer(self, puissance, duration=None, awaitIT=False):
        self.setOnForTime(puissance, True, duration, "both")

        if awaitIT and duration is not None:
            time.sleep(duration)

    def turnL(self, puissance, duration=None, awaitIT=False):
        self.setOnForTime(puissance, True, duration, "right")
        self.setOnForTime(0, False, duration, "left")

        if awaitIT and duration is not None:
            time.sleep(duration)

    def turnR(self, puissance, duration=None, awaitIT=False):
        self.setOnForTime(puissance, True, duration, "left")
        self.setOnForTime(0, False, duration, "right")

        if awaitIT and duration is not None:
            time.sleep(duration)

    def turnSelfL(self, puissance, duration=None, awaitIT=False):
        self.setOnForTime(puissance, True, duration, "right")
        self.setOnForTime(puissance, False, duration, "left")

        if awaitIT and duration is not None:
            time.sleep(duration)

    def turnSelfR(self, puissance, duration=None, awaitIT=False):
        self.setOnForTime(puissance, True, duration, "left")
        self.setOnForTime(puissance, False, duration, "right")

        if awaitIT and duration is not None:
            time.sleep(duration)
    
    def turnDL(self, puissance, duration=None, awaitIT=False):
        self.setOnForTime(puissance/2, False, duration, 'left')
        self.setOnForTime(puissance, False, duration, 'right')

        if awaitIT and duration is not None:
            time.sleep(duration)
    
    def turnDR(self, puissance, duration=None, awaitIT=False):
        self.setOnForTime(puissance, False, duration, 'left')
        self.setOnForTime(puissance/2, False, duration, 'right')

        if awaitIT and duration is not None:
            time.sleep(duration)
    
    def freiner(self):
        self.setOnForTime(1, True, None, "both")
        self.setOnForTime(1, False, None, "both")

    def arreter(self):
        self.setOnForTime(0, True, None, "both")
        self.setOnForTime(0, False, None, "both")

    def setOnForTime(self, value, back, duration=None, side="both"):
        if duration is None:
            duration = 1000000  # infinite duration :p

        def reset_state():
            while time.perf_counter() - self.lastTime < duration:
                time.sleep(0.1)  # Check periodically

            if side in ["both", "left"]:
                if back:
                    self.pBackWardL = 0
                else:
                    self.pForwardL = 0
            if side in ["both", "right"]:
                if back:
                    self.pBackWardR = 0
                else:
                    self.pForwardR = 0
            self.setEngines()

        if side in ["both", "left"]:
            if back:
                self.pBackWardL = value
            else:
                self.pForwardL = value
        if side in ["both", "right"]:
            if back:
                self.pBackWardR = value
            else:
                self.pForwardR = value

        self.lastTime = time.perf_counter()  # update last time
        self.setEngines()

        if self.rStateThread is None:
            self.rStateThread = threading.Thread(target=reset_state)
            self.rStateThread.start()

        elif self.rStateThread is not None and not self.rStateThread.is_alive():
            self.rStateThread = threading.Thread(target=reset_state)
            self.rStateThread.start()

    def setEngines(self):
        # Left engine
        if self.pForwardL > 0:
            self.Lengine.avancer(self.pForwardL * self.mulSpeed * self.mulSpeedL)
        elif self.pBackWardL > 0:
            self.Lengine.reculer(self.pBackWardL * self.mulSpeed * self.mulSpeedL)
        else:
            self.Lengine.arreter()

        # Right engine
        if self.pForwardR > 0:
            self.Rengine.avancer(self.pForwardR * self.mulSpeed * self.mulSpeedR)
        elif self.pBackWardR > 0:
            self.Rengine.reculer(self.pBackWardR * self.mulSpeed * self.mulSpeedR)
        else:
            self.Rengine.arreter()

    def Test(self):
        self.Lengine.Test()
        self.Rengine.Test()
        print("Test du moteur...")

        print("Avancer...")
        self.avancer(0.5, 2)
        time.sleep(2.5)

        print("Reculer...")
        self.reculer(0.5, 2)
        time.sleep(2.5)

        print("Tourner a gauche...")
        self.turnL(0.5, 2)
        time.sleep(2.5)

        print("Tourner a droite...")
        self.turnR(0.5, 2)
        time.sleep(2.5)

        print("Freiner...")
        self.freiner()
        time.sleep(2.5)

        print("Arreter...")
        self.arreter()

    def shutdown(self):
        self.arreter()
        self.Lengine.shutDown()
        self.Rengine.shutDown()


if __name__ == "__main__":
    rob = Robot()
    rob.Test()
