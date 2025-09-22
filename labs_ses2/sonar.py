from gpiozero import DigitalOutputDevice, DigitalInputDevice  # type: ignore
from time import perf_counter, sleep
from dels import Dels


class Sonar:

    VT_SON = 343.29
    FENETRE = 10 
    DIST_MIN = 1 #mètres
    
    def __init__(self, pinEcho, pinTrigger):
        self.__echo = DigitalInputDevice(pinEcho)
        self.__trigger = DigitalOutputDevice(pinTrigger)
        self.__echo.when_activated = self.when_activated
        self.__echo.when_deactivated = self.when_deactivated
        
        self.__pc_start = 0
        self.__distance = 0
        self.__valeurs_passees = []

    def trigger(self): #envoie l'onde avec un sleep d'une milliseconde
        self.__trigger.on()
        sleep(0.001)
        self.__trigger.off()

    def when_activated(self):
        #print("when_activated echo reçu")
        self.pc_start = perf_counter()
       
    def __calculer_moyenne_mobile(self, nouv_valeur): #prend une nouvelle valeur et vient calculer la moyenne
        valeurs_passees = self.__valeurs_passees
        valeurs_passees.append(nouv_valeur)
        
        if len(valeurs_passees)>self.FENETRE:
            del valeurs_passees[0]
            
        if len(valeurs_passees) > 2:
            MIN = min(valeurs_passees)
            MAX = max(valeurs_passees)  
            moyenne_mobile = (sum(valeurs_passees) - (MIN + MAX))/(len(valeurs_passees)-2)
        else:
            moyenne_mobile = sum(valeurs_passees)/len(valeurs_passees)
        
        self.__valeurs_passees = valeurs_passees
        
        return round(moyenne_mobile, 2)

    def when_deactivated(self):
        #print("when_deactivated echo finit")
        V_SON = self.VT_SON
        pc_stop = perf_counter()
        t = pc_stop - self.pc_start
        distance_actuelle = t * V_SON / 2        
        self.__distance = self.__calculer_moyenne_mobile(distance_actuelle) 
    
    def get_distance(self):
        #print('get distance mobile', f"{self.__distance}", 'm')
        return self.__distance
