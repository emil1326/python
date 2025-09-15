from gpiozero import DigitalOutputDevice, DigitalInputDevice  # type: ignore
from time import perf_counter, sleep


class Sonar:

    VT_SON = 0.343
    FENETRE = 10 
    
    def __init__(self, pinEcho, pinTrigger):
        self.__echo = DigitalInputDevice(pinEcho)
        self.__trigger = DigitalOutputDevice(pinTrigger, True, False)
        self.__echo.when_activated = self.when_activated
        self.__echo.when_deactivated = self.when_deactivated
        self.__pc_start = 0
        self.__distance = 0

    def trigger(self):
        self.__trigger.on()
        sleep(0.000001)
        self.__trigger.off()

    def when_activated(self):
        print("when_activated echo reçu")
        self.pc_start = perf_counter()

    def when_deactivated(self):
        print("when_deactivated echo finit")
        V_SON = self.VT_SON
        pc_stop = perf_counter()
        t = pc_stop - self.pc_start
        self.__distance = t * V_SON / 2
        print('distance', self.__distance, 'm')
        #TODO ajouter la moyenne mobile
    
    def get_distance(self):
        return self.__distance
