import gpiozero as gp  # type: ignore


class Dels:
    def __init__(self):
        self.__del_jaune = gp.DigitalOutputDevice(10)
        self.__del_verte = gp.DigitalOutputDevice(9)

    def allumer_jaune(self):
        self.__del_jaune.on()

    def allumer_verte(self):
        self.__del_verte.on()

    def eteindre(self):
        if self.__del_verte.value == 1:
            self.__del_verte.off()
        if self.__del_jaune.value == 1:
            self.__del_jaune.off()
