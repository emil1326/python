# gariel pereira levesque
from gab_moteurs import Moteur
from sonar import Sonar
from dels import Dels
from gab_orientation import Orientation, Etats


class Robot:
    def __init__(self,moteur_IN1=6, moteur_IN2=5, moteur_ENA=13, moteur_IN3=15, moteur_IN4=14, moteur_ENB=18, sonar=None, dels=None, orientation=None):
        print("init robot")
        self.orientation = orientation
        
        if dels is not None:
            self.__del_jaune = Dels(8)
            self.__del_verte = Dels(10)
        if sonar is not None:
            self.__sonar_g = Sonar(25, 8)
            self.__sonar_d = Sonar(20, 21)

        self.__moteur_g = Moteur(moteur_IN1, moteur_IN2, moteur_ENA)
        self.__moteur_d = Moteur(moteur_IN3, moteur_IN4, moteur_ENB)

    # voiture
    def avancer(self, vitesse=1.0):
        if self.orientation is not None:
            self.orientation.set_etat(Etats.avance)
        self.__moteur_d.avancer(vitesse)
        self.__moteur_g.avancer(vitesse)

    def reculer(self):
        if self.orientation is not None:
            self.orientation.set_etat(True)
        self.__moteur_d.reculer(1)
        self.__moteur_g.reculer(1)

    def tourner_gauche(self, vitesse=1.0):
        if self.orientation is not None:
            self.orientation.set_tourne(True)
        self.__moteur_d.avancer(vitesse)
        self.__moteur_g.reculer(vitesse)

    def tourner_droite(self, vitesse=1.0):
        if self.orientation is not None:
            self.orientation.set_tourne(True)
        self.__moteur_d.reculer(vitesse)
        self.__moteur_g.avancer(vitesse)

    def diagonale_droite(self):
        if self.orientation is not None:
            self.orientation.set_tourne(True)
            self.orientation.set_avance(True)
        self.__moteur_d.avancer(0.1)
        self.__moteur_g.avancer(1)

    def diagonale_gauche(self):
        if self.orientation is not None:
            self.orientation.set_tourne(True)
            self.orientation.set_avance(True)
        self.__moteur_d.avancer(1)
        self.__moteur_g.avancer(0.1)

    def arreter(self):
        if self.orientation is not None:
            self.orientation.set_avance(False)
            self.orientation.set_tourne(False)
        self.__moteur_d.arreter()
        self.__moteur_g.arreter()

    def modifier_vitesse(self, multiplicateur):
        self.__moteur_d.addMulSpeed(multiplicateur)
        self.__moteur_g.addMulSpeed(multiplicateur)

    def shutdown(self):
        if self.__del_jaune is not None:
            self.__del_jaune.shutdown()
        if self.__del_verte is not None:
            self.__del_verte.shutdown()
        if self.__sonar_d is not None:
            self.__sonar_d.shutdown()
        if self.__sonar_g is not None:
            self.__sonar_g.shutdown()
        if self.orientation is not None:
            self.orientation.set_tourne(False)
            self.orientation.set_avance(False)
            self.orientation.stop()

    # sonars
    def trigger_sonars(self):
        if self.__sonar_d is not None:
            self.__sonar_d.demarrer_trigger()
        if self.__sonar_g is not None:
            self.__sonar_g.demarrer_trigger()

    def arreter_sonars(self):
        if self.__sonar_d is not None:
            self.__sonar_d.arreter_trigger()
        if self.__sonar_g is not None:
            self.__sonar_g.arreter_trigger()
            
    def get_distance(self, sonar):
        if self.__sonar_g is not None and sonar == "g":  # sonar de gauche
            return self.__sonar_g.get_distance()
        if self.__sonar_d is not None and sonar == "d":  # sonar de droite
            return self.__sonar_d.get_distance()
        else:
            return -1

    # dels
    def clignoter_del_jaune(self, t_clign):
        if self.__del_jaune is not None:
            self.__del_jaune.partir_clignotement(t_clign)

    def clignoter_del_verte(self, t_clign):
        if self.__del_verte is not None:
            self.__del_verte.partir_clignotement(t_clign)
    def arreter_clignoter_del_jaune(self):
        if self.__del_jaune is not None:
            self.__del_jaune.arreter_clignotement()

    def arreter_clignoter_del_verte(self):
        if self.__del_verte is not None:
            self.__del_verte.arreter_clignotement()