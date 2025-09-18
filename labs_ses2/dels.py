import gpiozero as gp  # type: ignore
import time as t

class Dels:
    
    T_CLIGN = 0.5
    
    def __init__(self):
        self.__del_jaune = gp.DigitalOutputDevice(10)
        self.__del_verte = gp.DigitalOutputDevice(9)
        self.__stop_clignottement = True

    def arreter_clignotement(self):
        self.__stop_clignottement = False
    
    def clignoter_dels(self):
        while not self.__stop_clignottement:
            self.allumer_jaune()
            self.allumer_verte()
            t.sleep(0.5)
            self.eteindre()
    
    def allumer_jaune(self):
        self.__del_jaune.on()

    def allumer_verte(self):
        self.__del_verte.on()

    def eteindre(self):
        if self.__del_verte.value == 1:
            self.__del_verte.off()
        if self.__del_jaune.value == 1:
            self.__del_jaune.off()
