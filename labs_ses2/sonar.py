from gpiozero import DigitalOutputDevice, DigitalInputDevice  # type: ignore
from time import perf_counter, sleep
from dels import Dels
import threading


class Sonar:

    VT_SON = 343.29
    FENETRE = 10
    DIST_MIN = 1  # mètres

    def __init__(self, pinEcho, pinTrigger):
        self.__trigger = DigitalOutputDevice(pinTrigger)

        self.__echo = DigitalInputDevice(pinEcho)
        self.__echo.when_activated = self.when_activated
        self.__echo.when_deactivated = self.when_deactivated

        # flags et thread
        self.__continuer_trigger = True
        self.__stop_thread = threading.Event()
        self.__thread_trigger = threading.Thread(target=self.trigger)
        self.__thread_trigger.start()

        # initialisation des atttributs privés
        self.__pc_start = 0
        self.__distance = 0
        self.__valeurs_passees = []

    def trigger(self):  # envoie l'onde
        while not self.__stop_thread.is_set():
            if self.__continuer_trigger:
                self.__trigger.on()
                sleep(0.001)  # sleep d'une milliseconde
                self.__trigger.off()
            sleep(0.5)  # sleep pour partir l'onde 1x/seconde

    def demarrer_trigger(self):
        self.__continuer_trigger = True

    def arreter_trigger(self):
        self.__continuer_trigger = False

    def when_activated(self):
        self.__pc_start = perf_counter()

    def __calculer_moyenne_mobile(
        self, nouv_valeur
    ):  # prend une nouvelle valeur et vient calculer la moyenne mobile
        self.__valeurs_passees.append(
            nouv_valeur
        )  # ajoute la nouvelle distance a la fin du tableau

        if (
            len(self.__valeurs_passees) > self.FENETRE
        ):  # si la longueur est plus grande que notre fenêtre
            del self.__valeurs_passees[0]  # supprimer la première valeur

        if (
            len(self.__valeurs_passees) > 2
        ):  # si la longueur du tableau est plus grande que 2
            MIN = min(self.__valeurs_passees)
            MAX = max(self.__valeurs_passees)
            moyenne_mobile = (sum(self.__valeurs_passees) - (MIN + MAX)) / (
                len(self.__valeurs_passees) - 2
            )  # on calcul la moyenne avec le minimum et le maximum pris en compte
        else:  # s'il est plus petit ou égal à 2
            moyenne_mobile = sum(self.__valeurs_passees) / len(
                self.__valeurs_passees
            )  # on calcul la moyenne sans le minimum et le maximum

        return moyenne_mobile

    def when_deactivated(self):  # quand le echo a finit
        pc_stop = perf_counter()
        t = pc_stop - self.__pc_start  # calcul du temps écoulé
        distance_actuelle = t * self.VT_SON / 2  # calcul de la distance
        self.__distance = self.__calculer_moyenne_mobile(
            distance_actuelle
        )  # on attribut une distance moyenne

    def get_distance(self):  # getter pour acceder à la distance moyenne
        # print('get distance mobile', f"{self.__distance}", 'm')
        return self.__distance

    # arret propre du thread
    def shutdown(self):
        self.__stop_thread.set()
        self.__thread_trigger.join()
