import threading
import time
from gpiozero import PWMOutputDevice  # type: ignore
from gpiozero import DigitalOutputDevice  # type: ignore


class Moteur:
    # in1, in2, enA, in3, in4, enB
    allowedPort = [6, 5, 13, 15, 14, 18]

    # portAvancer = portReculer = portPuissance = None

    # pForward = 0  # internal puissance back && forth
    # pBackWard = 0

    def __init__(self, portAvancer, portReculer, portPuissance):
        if portAvancer in self.allowedPort:
            self.portAvancer = DigitalOutputDevice(portAvancer)
        if portReculer in self.allowedPort:
            self.portReculer = DigitalOutputDevice(portReculer)
        if portPuissance in self.allowedPort:
            self.portPuissance = PWMOutputDevice(portPuissance)

        self.pForward = 0
        self.pBackWard = 0

        self.lastTime = time.perf_counter()
        self.rStateThread = None  # Initialize with None

    def avancer(self, puissance, duration=None):
        self.setOnForTime(puissance, False, duration)

    def reculer(self, puissance, duration=None):
        self.setOnForTime(puissance, True, duration)

    def freiner(self):
        self.setOnForTime(1, True, None)
        self.setOnForTime(1, False, None)

    def arreter(self):
        self.setOnForTime(0, True, None)
        self.setOnForTime(0, False, None)

    def setOnForTime(self, value, back, duration=None):
        if duration is None:
            duration = 1000000  # infinite duration

        # rajoutte un obj comme variable a rajouter tsu la classe pour sa marche ben
        tmp = object()
        self._lastToken = tmp

        def reset_state(my_token):
            start_time = time.perf_counter()
            while time.perf_counter() - start_time < duration:
                time.sleep(0.05)
            # reset quand c le dernier call
            if getattr(self, "_lastToken", None) is my_token:
                if back:
                    self.pBackWard = 0
                else:
                    self.pForward = 0
                self.setEngine()

        if back:
            self.pBackWard = value
        else:
            self.pForward = value
        self.setEngine()

        t = threading.Thread(target=reset_state, args=(tmp,))
        t.start()

    def setEngine(self):
        if self.pForward > self.pBackWard:
            self.portAvancer.on()
            self.portReculer.off()
            self.portPuissance.value = self.pForward
        if self.pForward < self.pBackWard:
            self.portAvancer.off()
            self.portReculer.on()
            self.portPuissance.value = self.portReculer

    def Test(self):
        print("Test du moteur...")
        self.avancer(0.5, 2)
        time.sleep(2.5)
        self.reculer(0.5, 2)
        time.sleep(2.5)
        self.arreter()

    def shutDown(self):
        self.arreter()

        print("shutdown")


if __name__ == "__main__":
    mot = Moteur(6, 5, 13)
    mot.Test()
    mot = Moteur(15, 14, 18)
    mot.Test()
