from gab_moteurs import Moteur
from sonar import Sonar
from dels import Dels
from camera import Camera
import time


class Robot:
    def __init__(self, sonar=None, dels=None):
        if dels is not None:
            self.__del_jaune = Dels(8)
            self.__del_verte = Dels(10)
        if sonar is not None:
            self.__sonar_g = Sonar(25, 8)
            self.__sonar_d = Sonar(20, 21)

        self.__moteur_g = Moteur(6, 5, 13)
        self.__moteur_d = Moteur(15, 14, 18)

        self.__stop_sonar = True

    # voiture
    def avancer(self, vitesse=1.0):
        self.__moteur_d.avancer(vitesse)
        self.__moteur_g.avancer(vitesse)

    def reculer(self):
        self.__moteur_d.reculer(1)
        self.__moteur_g.reculer(1)

    def tourner_gauche(self, vitesse):
        self.__moteur_d.avancer(vitesse)
        self.__moteur_g.reculer(vitesse)

    def tourner_droite(self, vitesse):
        self.__moteur_d.reculer(vitesse)
        self.__moteur_g.avancer(vitesse)

    def diagonale_droite(self):
        self.__moteur_d.avancer(0.1)
        self.__moteur_g.avancer(1)

    def diagonale_gauche(self):
        self.__moteur_d.avancer(1)
        self.__moteur_g.avancer(0.1)

    def arreter(self):
        self.__moteur_d.arreter()
        self.__moteur_g.arreter()

    def modifier_vitesse(self, multiplicateur):
        self.__moteur_d.addMulSpeed(multiplicateur)
        self.__moteur_g.addMulSpeed(multiplicateur)

    def shutdown(self):
        if self.__del_jaune:
            self.__del_jaune.shutdown()
        if self.__del_verte:
            self.__del_verte.shutdown()
        if self.__sonar_d is not None:
            self.__sonar_d.shutdown()
        if self.__sonar_g is not None:
            self.__sonar_g.shutdown()

    # sonars
    def trigger_sonars(self):
        self.__sonar_d.demarrer_trigger()
        self.__sonar_g.demarrer_trigger()

    def arreter_sonars(self):
        self.__sonar_d.arreter_trigger()
        self.__sonar_g.arreter_trigger()

    def get_distance(self, sonar):
        if sonar == "g":  # sonar de gauche
            return self.__sonar_g.get_distance()
        if sonar == "d":  # sonar de droite
            return self.__sonar_d.get_distance()
        else:
            return -1

    # dels
    def clignoter_del_jaune(self, t_clign):
        self.__del_jaune.partir_clignotement(t_clign)

    def clignoter_del_verte(self, t_clign):
        self.__del_verte.partir_clignotement(t_clign)

    def arreter_clignoter_del_jaune(self):
        self.__del_jaune.arreter_clignotement()

    def arreter_clignoter_del_verte(self):
        self.__del_jaune.arreter_clignotement()
