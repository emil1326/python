import gpiozero as gp  # type: ignore
import time as t

class Dels:
    
    T_CLIGN = 0.5
    
    def __init__(self):
        self.__del_jaune = gp.DigitalOutputDevice(10)
        self.__del_verte = gp.DigitalOutputDevice(9)
        self.__stop_clignottement = True
    
    def allumer_jaune(self):
        self.__del_jaune.on()

    def allumer_verte(self):
        self.__del_verte.on()

    def eteindre(self):
        self.__del_verte.off()
        self.__del_jaune.off()
