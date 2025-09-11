from gpiozero import DigitalOutputDevice, DigitalInputDevice  # type: ignore
from time import perf_counter


class Sonar:

    def _init(self, pinEcho, pinTrigger):
        self.echo = DigitalInputDevice(pinEcho)
        self.trigger = DigitalOutputDevice(pinTrigger, True, False)
        self.echo.when_activated = self.when_activated
        self.echo.when_deactivated = self.when_deactivated
        self.pc_start = 0
        self.distance = 0

    def when_activated(self):
        print("echo activated")
        self.pc_start = perf_counter()

    def when_deactivated(self):
        pc_stop = perf_counter()
        t = pc_stop - self.pc_start
        v = 0.343
        self.distance = t * v / 2
