import grovepi # type: ignore
import time


class DetecteurDeJour:
    JOUR_LIMITE = 40
    PERIODE = 5  # 5 secondes d'hystérésis
    JourNuit = None # fallais le rajouter aussi, maque une classe ou qqch avc une valuer dedans, surement classe de config?
    
    def __init__(self, port):
        self.__port = port
        self.__jour = None
        self.__debut_jour = None
        self.JourNuit = Journuit # faillais je le rajoute pcq aussinon sa fait pas de sens

    def lire_valeur(self):
        return grovepi.analogRead(self.__port)

    def est_jour(self):
        valeur = self.lire_valeur()
        # si curr light est plus grand que se qui est considerer comme le debut du jour
        if valeur > self.JourNuit.JOUR_LIMITE: # type: ignore  -> supress warning
            if self.__debut_jour is None:
                self.__debut_jour = time.perf_counter()
            
            # if is day for enough time
            elif self.__debut_jour > time.perf_counter - self.JourNuit.Wait_TIME:  # type: ignore
              self.__jour = True
            else:
              self.__jour = False
              
            self.__debut_jour = time.perf_counter()
            
        return self.__jour

class Journuit:
  JOUR_LIMITE = 0
  Wait_TIME = 10