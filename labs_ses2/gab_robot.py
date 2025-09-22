from gab_moteurs import Moteur
from sonar import Sonar
from dels import Dels
import time

class Robot:
    
    def __init__(self, sonar = None, dels = None):
        if(dels):
            self.__dels = Dels()
        if(sonar):
            self.__sonar_g = Sonar(25, 8)
            self.__sonar_d = Sonar(20, 21)
        
        self.__moteur_g = Moteur(6, 5, 13)
        self.__moteur_d = Moteur(15, 14, 18)
        self.__stop_clignotement = True
        self.__stop_sonar = True
        
    
    def avancer(self):
        self.__moteur_d.avancer(1)
        self.__moteur_g.avancer(1)
    
    def reculer(self):
        self.__moteur_d.reculer(1)
        self.__moteur_g.reculer(1)
    
    def tourner_gauche(self):
        self.__moteur_d.avancer(1)
        self.__moteur_g.reculer(1)
    
    def tourner_droite(self):
        self.__moteur_d.reculer(1)
        self.__moteur_g.avancer(1)
    
    def diagonale_droite(self):
        self.__moteur_d.avancer(0.4)
        self.__moteur_g.avancer(1)
    
    def diagonale_gauche(self):
        self.__moteur_d.avancer(1)
        self.__moteur_g.avancer(0.4)
    
    def arreter(self):
        self.__moteur_d.arreter()
        self.__moteur_g.arreter()
    
    def modifier_vitesse(self, multiplicateur):
        self.__moteur_d.addMulSpeed(multiplicateur)
        self.__moteur_g.addMulSpeed(multiplicateur)
    
    def trigger_sonar_g(self):
        while not self.__stop_sonar:
            self.__sonar_g.trigger()
            time.sleep(0.1)
    
    def trigger_sonar_d(self):
        while not self.__stop_sonar:
            self.__sonar_d.trigger()        
            time.sleep(0.1)
    
    def arreter_sonars(self):
        self.__stop_sonar = True
    
    def arreter_clignoter_dels(self):
        self.__stop_clignotement = True
    
    def clignoter_dels(self):
        while not self.__stop_clignotement:
            self.__dels.allumer_jaune()
            self.__dels.allumer_verte()
            time.sleep(0.5)
            self.__dels.eteindre()
    
    def dels_clignotent(self):
        return not self.__stop_clignotement
    
    def get_distance(self, sonar=None):
        if sonar == 'g': #sonar de gauche
            return self.__sonar_g.get_distance()
        if sonar == 'd': #sonar de droite
            return self.__sonar_d.get_distance()
        elif sonar == None: #les deux
            d_g = self.__sonar_g.get_distance()
            d_d = self.__sonar_d.get_distance()
            
            return (d_g + d_d) / 2 #retourn la moyenne entre les deux
        
        