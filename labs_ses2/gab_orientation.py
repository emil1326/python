import time
import math
from threading import Thread, Event
from collections import deque
from icm20948 import ICM20948  # type: ignore
import time
import enum

class Etats(enum.Enum):
    immobile = 0
    avance = 1
    tourne = 2


class Orientation:    
    FENETRE = 50
    VITESSE_ROBOT = 0.6
    CALIBRATION_SEC = 6.0
    
    def __init__(self):
        self.__imu = ICM20948()        
        self.__etat_courant = Etats.immobile
        
        self.__tab_gx = []
        self.__gx_biais = 0.0

        self.__angle_x = 0.0
        self.__gx_prec = None
        self.__temps_prec = None

        self.__my_corr = 0.0
        self.__mz_corr = 0.0

        self.__orientation = 0.0

        self.__event_thread = Event()
        self.__event_thread.clear()
        self.__boucle = Thread(target=self.calculer_orientation, daemon=True)
        
        self.__maintenir_cap_event = Event()
        self.__maintenir_cap_event.clear()
        self.__maintenir_cap_thread = Thread(target=self.maintenir_cap, daemon=True)
    
    def demarrer(self, robot):
        try:
            robot.tourner_gauche(self.VITESSE_ROBOT)
            self.calibrer_magnetometre()
            robot.arreter()
            self.__event_thread.set()
            self.__boucle.start()
            return True
        except:
            print("Impossible de demarrer le service dorientation")

    
    def arreter(self):
        self.__event_thread.clear()
        self.__boucle.join()
        self.__maintenir_cap_event.clear()
        self.__maintenir_cap_thread.join()
    
    def calibrer_magnetometre(self):
        my_valeurs, mz_valeurs = [], []
        debut = time.time()
        
        while time.time() - debut < self.CALIBRATION_SEC:
            _, my, mz = self.imu.read_magnetometer_data()
            my_valeurs.append(my)
            mz_valeurs.append(mz)
            time.sleep(0.02)

        if my_vals and mz_vals:
            self.__my_corr = (max(my_valeurs) + min(my_valeurs)) / 2.0
            self.__mz_corr = (max(mz_valeurs) + min(mz_valeurs)) / 2.0

        print(f"Calibration: corr_my={self.__:.3f}, corr_mz={self.corr_mz:.3f}")
    
    def calculer_orientation(self):
        while self.__event_thread.is_set():
            temps_cour = time.time()

            ax, ay, az, gx, gy, gz = self.__imu.read_accelerometer_gyro_data()
            mx, my, mz = self.__imu.read_magnetometer_data()

            my_corrigé = my - self.__my_corr
            mz_corrigé = mz - self.__mz_corr
            rad = math.atan2(mz_corrigé, my_corrigé)
            self.__cap = rad * (180/math.pi)

            if self.__etat_courant == Etats.immobile:
                self.__tab_gx.append(gx)
                if len(self.__tab_gx) > FENETRE:
                    self.__tab_gx.pop(0)
                self.__gx_biais = sum(self.__tab_gx) / len(self.__tab_gx) if self.__tab_gx else 0.0

                self.__gx_prec = None
                self.__temps_prec = None

            elif self.__etat_courant == Etats.tourne:
                gx_corr = gx - self.__gx_biais
                if self.__gx_prec is None:
                    # première mesure après l’immobilité; pas d’intégration
                    self.__gx_prec = gx_corr
                    self.__temps_prec = temps_cour
                else:# intégrale
                    dt = temps_cour - self.__temps_prec
                    self.__angle_x += dt * (gx_corr + self.__gx_prec)/2
                    self.__angle_x %= 360
                    self.__gx_prec = gx_corr
                    self.__temps_prec = temps_cour

            print(f"Orientation={self.__cap:.1f}°, relative={self.__angle_x:.1f}°")
            time.sleep(0.01)
    
    def set_etat(self, nouv_etat):
        if nouv_etat in Etats.mro():
            self.__etat_courant = nouv_etat
        else:
            print('Nouvel état invalide')
    
    def get_orientation(self):
        return self.__cap

    def set_maintenir_cap(self, etat:bool):
        if(etat):
            self.__maintenir_cap.set()
            
        else:
            self.__maintenir_cap.clear()
    
    def maintenir_cap(self, cap):
        while self.__maintenir_cap.is_set():
            angle_actuel = get_orientation()
            diff = (cap - angle_actuel + 180) % 360 - 180
            time.sleep(0.05)
            print("maintenir cap diff:", diff)
        
        
