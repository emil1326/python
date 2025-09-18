import gpiozero as gp  # type: ignore

class Dels:
    
    T_CLIGN = 0.5
    
    def __init__(self):
        self.__del_jaune = gp.DigitalOutputDevice(10)
        self.__del_verte = gp.DigitalOutputDevice(9)

    def clignoter_jaune(self):
        self.__del_jaune.blink(on_time=self.T_CLIGN, off_time=self.T_CLIGN)
    
    def clignoter_verte(self):
        self.__del_verte.blink(on_time=self.T_CLIGN, off_time=self.T_CLIGN)
    
    def allumer_jaune(self):
        self.__del_jaune.on()

    def allumer_verte(self):
        self.__del_verte.on()

    def eteindre(self):
        if self.__del_verte.value == 1:
            self.__del_verte.off()
        if self.__del_jaune.value == 1:
            self.__del_jaune.off()
