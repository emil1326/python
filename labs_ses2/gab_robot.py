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
        
        self.__stop_sonar = True
        
    
    def avancer(self, vitesse = 1):
        self.__moteur_d.avancer(vitesse)
        self.__moteur_g.avancer(vitesse)
    
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
    
    def trigger_sonars(self):
        self.__sonar_d.demarrer_trigger()
        self.__sonar_g.demarrer_trigger()
    
    def arreter_sonars(self):
        self.__sonar_d.arreter_trigger()
        self.__sonar_g.arreter_trigger()
    
    def clignoter_del_jaune(self, t_clign):
        self.__dels.partir_clignotement_jaune(t_clign)
    
    def clignoter_del_verte(self, t_clign):
        self.__dels.partir_clignotement_verte(t_clign)
    
    def arreter_clignoter_del_jaune(self):
        self.__dels.arreter_clignotement_jaune()
    
    def arreter_clignoter_del_verte(self):
        self.__dels.arreter_clignotement_verte()
    
    def get_distance(self, sonar):
        if sonar == 'g': #sonar de gauche
            return self.__sonar_g.get_distance()
        if sonar == 'd': #sonar de droite
            return self.__sonar_d.get_distance()
        else:
            return -1
    
    def shutdown(self):
        if self.__dels:
            self.__dels.shutdown()
        if self.__sonar_d:
            self.__sonar_d.shutdown()
        if self.__sonar_g:
            self.__sonar_g.shutdown()
            
        
        