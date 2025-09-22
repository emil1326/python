import gpiozero as gp  # type: ignore
import time as t
from threading import Thread

class Dels:
    
    T_CLIGN = 0.5
    
    def __init__(self):
        self.__del_jaune = gp.DigitalOutputDevice(10)
        self.__del_verte = gp.DigitalOutputDevice(9)
        self.__clignoter_jaune = False
        self.__clignoter_verte = False
        self.__thread_del_jaune = Thread(target=self.clignoter_del_jaune)
        self.__thread_del_verte = Thread(target=self.clignoter_del_verte)   
    
    
    def allumer_jaune(self):
        self.__del_jaune.on()

    def allumer_verte(self):
        self.__del_verte.on()

    def eteindre_verte(self):
        self.__del_verte.off()
        
    def eteindre_jaune(self):
        self.__del_jaune.off()
        
    def arreter_clignoter_del_jaune(self):
        self.__clignoter_jaune = False
    
    def arreter_clignoter_del_verte(self):
        self.__clignoter_verte = False
    
    def clignoter_del_jaune(self):
        self.__clignoter_jaune = True
        while self.__clignoter_jaune:
            self.allumer_jaune()
            t.sleep(self.T_CLIGN)
            self.eteindre_jaune()
            t.sleep(self.T_CLIGN)
            
    def clignoter_del_verte(self):
        self.__clignoter_verte = True
        while self.__clignoter_verte:
            self.allumer_verte()
            t.sleep(self.T_CLIGN)
            self.eteindre_verte()
            t.sleep(self.T_CLIGN)
            
##TODO thread part 2x
    
    def partir_clignotement_jaune(self):
        if self.__thread_del_jaune is None or not self.__thread_del_jaune.is_alive():
            self.__thread_del_jaune.start()
    
    def partir_clignotement_verte(self):
        if self.__thread_del_verte is None or not self.__thread_del_verte.is_alive():
            self.__thread_del_verte.start()
    
    def shutdown_threads(self):
        self.__thread_del_jaune.join()
        self.__thread_del_verte.join()
