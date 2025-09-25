import threading
import time as t
import gpiozero as gp

class Dels:

    def __init__(self):
        # DELs
        self.__del_jaune = gp.DigitalOutputDevice(10)
        self.__del_verte = gp.DigitalOutputDevice(9)
        
        # flags pour clignotement
        self.__clignoter_jaune = False
        self.__clignoter_verte = False
        
        #temps de clignotement
        self.__t_clign_jaune = 0.5
        self.__t_clign_verte = 0.5
        
        # event pour arrêter proprement les threads
        self.__stop_event = threading.Event()
        
        # threads
        self.__thread_del_jaune = threading.Thread(target=self._clignoter_del_jaune)
        self.__thread_del_verte = threading.Thread(target=self._clignoter_del_verte)
        self.__thread_del_jaune.start()
        self.__thread_del_verte.start()
    
    # méthodes DELs simples
    def allumer_jaune(self):
        self.__del_jaune.on()

    def eteindre_jaune(self):
        self.__del_jaune.off()

    def allumer_verte(self):
        self.__del_verte.on()

    def eteindre_verte(self):
        self.__del_verte.off()
    
    # méthodes clignotement
    def partir_clignotement_jaune(self, t_clign):
        self.__t_clign_jaune = t_clign
        self.__clignoter_jaune = True
    
    def arreter_clignotement_jaune(self):
        self.__clignoter_jaune = False

    def partir_clignotement_verte(self, t_clign):
        self.__t_clign_verte = t_clign
        self.__clignoter_verte = True
    
    def arreter_clignotement_verte(self):
        self.__clignoter_verte = False
    
    # threads permanents
    def _clignoter_del_jaune(self):
        while not self.__stop_event.is_set():
            if self.__clignoter_jaune:
                self.allumer_jaune()
                t.sleep(self.__t_clign_jaune)
                self.eteindre_jaune()
                t.sleep(self.__t_clign_jaune)
            else:
                t.sleep(0.5)
    
    def _clignoter_del_verte(self):
        while not self.__stop_event.is_set():
            if self.__clignoter_verte:
                self.allumer_verte()
                t.sleep(self.__t_clign_verte)
                self.eteindre_verte()
                t.sleep(self.__t_clign_verte)
            else:
                t.sleep(0.5)

    # arrêt propre des threads
    def shutdown(self):
        self.__stop_event.set()
        self.__thread_del_jaune.join()
        self.__thread_del_verte.join()

