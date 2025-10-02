import threading
import time as t
import gpiozero as gp  # type: ignore


class Dels:

    def __init__(self, port_del):
        # DELs
        self.__del = gp.DigitalOutputDevice(port_del)

        # flags pour clignotement
        self.__clignote = False

        # temps de clignotement
        self.__t_clign = 0.5

        # event pour arrêter proprement les threads
        self.__stop_event = threading.Event()

        # threads
        self.__thread_del = threading.Thread(target=self._clignoter_del)
        self.__thread_del.start()

    # méthodes DELs simples
    def allumer(self):
        self.__del.on()

    def eteindre(self):
        self.__del.off()

    # méthodes clignotement
    def partir_clignotement(self, t_clign):
        self.__t_clign = t_clign
        self.__clignote = True

    def arreter_clignotement(self):
        self.__clignote = False

    # threads permanents
    def _clignoter_del(self):
        while not self.__stop_event.is_set():
            if self.__clignote:
                self.allumer()
                t.sleep(self.__t_clign)
                self.eteindre()
                t.sleep(self.__t_clign)
            else:
                t.sleep(0.5)
                
    # arrêt propre des threads
    def shutdown(self):
        self.__stop_event.set()
        self.__thread_del.join()
