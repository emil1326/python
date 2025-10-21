# file: labs_ses2/exammises.py
# description: classes et fonctions pour la gestion de la caméra et des encodeurs de rotation
# auteur: Emilien devauchelle
# date: 20 octobre 2025

# imports

import cv2  # type: ignore
import numpy as np  # type: ignore
from gpiozero import DigitalInputDevice  # type: ignore

# from gab_robot.py import Robot

# classes

# ici pour que tout soit dans un seul fichier


class Camera:
    # constantes
    # resolution de l'image
    LARGEUR = 640
    HAUTEUR = 480
    # limites
    MIN_HUE = 0
    MAX_HUE = 255
    MIN_SAT = 0
    MAX_SAT = 255
    MIN_VAL = 0
    MAX_VAL = 255
    CORRELATION_MIN = 0.65
    ROI = 50

    def __init__(self):
        self.__cam = None
        self.__derniere_position_objet = None

        """ if platform.system() == "Linux": 
            from picamera2 import Picamera2 # type: ignore   
            self.__cam = Picamera2()
            config = self.__cam.create_video_configuration(
                main={"format": "RGB888", "size": (LARGEUR, HAUTEUR)}
            )
            self.__cam.configure(config)
            self.__cam.start()        
        elif platform.system() == "Windows": """
        self.__cam = cv2.VideoCapture(1)
        self.__cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.LARGEUR)
        self.__cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HAUTEUR)
        self.__cam.read()

    # nous laisse resetter la camera setting quand on veut pas ceux de base -> unused pcq literals
    def resetCamera(self):
        self.__cam = cv2.VideoCapture(1)
        self.__cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.LARGEUR)
        self.__cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HAUTEUR)
        self.__cam.read()

    # prend une touche d'arrêt pour stopper la boucle et le nom dans lequel le modèle doit être sauvegardé
    def creation_du_model(self, touche_arret, nom_fichier):
        touche_presse = ""
        img_gray = None
        while touche_arret != touche_presse:
            img_bgr = self.capturer_image_bgr()
            img_gray = self.convertir_image_bgr2gray(img_bgr)

            cv2.imshow("Creation du model", img_gray)

            touche = cv2.waitKey(30)

            if touche == -1 or touche > 255:
                continue

            touche_presse = chr(touche)  # image capturé

        cv2.destroyAllWindows()
        cv2.imwrite(nom_fichier, img_gray)

    # prend un masque du model et retourne l'image en couleur avec des rectangles dessines si un model est trouve
    def rechercher_model(self, nom_model):
        model = cv2.imread(nom_model, cv2.IMREAD_GRAYSCALE)

        ymin = 0
        ymax = self.HAUTEUR
        xmin = 0
        xmax = self.LARGEUR

        touche_presse = ""

        while touche_presse != "x":
            img_bgr = self.capturer_image_bgr()
            img_gray = self.convertir_image_bgr2gray(img_bgr)
            img_cible = img_gray

            if self.__derniere_position_objet is not None:
                ymin = self.__derniere_position_objet["y"] - self.ROI
                ymax = (
                    self.__derniere_position_objet["y"] + model.shape[0] + self.ROI
                )  # hauteur
                xmin = self.__derniere_position_objet["x"] - self.ROI
                xmax = (
                    self.__derniere_position_objet["x"] + model.shape[1] + self.ROI
                )  # largeur

                # bornes dans les dimensions valides
                h, w = img_gray.shape
                ymin = max(0, ymin)
                xmin = max(0, xmin)
                ymax = min(h, ymax)
                xmax = min(w, xmax)

                img_cible = img_gray[ymin:ymax, xmin:xmax]

            res_match = cv2.matchTemplate(img_cible, model, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(res_match)

            print(
                f"max_val={max_val:.3f} à {max_loc}, "
                f"img_cible={img_cible.shape}, "
                f"model={model.shape}"
            )

            if self.CORRELATION_MIN < max_val:
                x = max_loc[0] + xmin
                y = max_loc[1] + ymin
                self.__derniere_position_objet = {"y": y, "x": x}
                # dessiner le rectangle autour de l'objet détecté
                cv2.rectangle(
                    img_bgr,
                    (x, y),
                    (x + model.shape[1], y + model.shape[0]),
                    (0, 0, 255),
                    2,
                )

            # dessiner le rectangle du ROI
            cv2.rectangle(img_bgr, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)
            cv2.imshow("Lab 4 | Recherche du model", img_bgr)

            key = cv2.waitKeyEx(30)  # attendre 30ms pour l'appui d'une touche

            # gestion d'erreur
            if key == -1 or key > 255:
                continue

            touche_presse = chr(key)
        print("arrêt de la recherche")

    def convertir_image_bgr2gray(self, image_bgr):
        return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # dessine un rectangle sur l'image passée autour d'un contour passé en paramètre
    def dessiner_rectangle_sur_image(
        self, image, contour, couleur=(0, 0, 255), epaisseur=2
    ):
        # si aucun contour a dessiner on quitte la fonction
        if contour is None or len(contour) == 0:
            return
        x, y, l, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + l, y + h), couleur, epaisseur)

    # Retourne aire, centre (x, y) d'un contour
    def get_dimensions_contour(self, contour):
        x, y, l, h = cv2.boundingRect(contour)
        aire = l * h
        centre = {"x": x + (l // 2), "y": y + (h // 2)}

        return aire, centre

    # prend une image binarisée et retourne le plus gros blob
    def get_plus_gros_contour(self, image_bin):
        # définition des maximums
        plus_gros_contour = None
        max_aire = 0

        contours, _ = cv2.findContours(
            image_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )

        # pour chaque contour
        for c in contours:
            # prendre les dimensions
            x, y, l, h = cv2.boundingRect(c)
            # calculer l'aire
            aire = l * h
            # si l'aire est le plus grand
            if aire > max_aire:
                max_aire = aire
                # c'est alors aussi le plus gros contour
                plus_gros_contour = c

        return plus_gros_contour

    # prend une image hsv et la binarise
    def binariser_image(self, image_hsv):
        # définition des bornes
        borne_min = np.array([self.MIN_HUE, self.MIN_SAT, self.MIN_VAL])
        borne_max = np.array([self.MAX_HUE, self.MAX_SAT, self.MAX_VAL])

        # création du masque
        masque = cv2.inRange(image_hsv, borne_min, borne_max)

        return masque

    # prend une image BGR et la binarise
    def binariser_image_BGR(self, image_BGR):
        # définition des bornes
        borne_min = np.array([0, 0, 128])
        borne_max = np.array([255, 255, 255])

        # création du masque
        masque = cv2.inRange(image_BGR, borne_min, borne_max)

        return masque

    def convertir_image_bgr2hsv(self, image_bgr):
        image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        return image_hsv

    # capture et retourne une image (tableau) en source bgr
    def capturer_image_bgr(self):
        """if platform.system() == "Linux":
            return self.__cam.capture_array()
        elif platform.system() == "Windows":"""
        ret, image = self.__cam.read()  # type: ignore
        return image


class encodeurDeRotation:

    # diametre 6.5cm
    # (6.5 * 3.14159) / 80 -> roue robot
    # TAILLE_ROUE = 0.5
    STOP_LENGTH = 0

    # 22 , 27
    def __init__(self, capteur_droit=None, capteur_gauche=None):
        if capteur_droit is not None:
            self.CapteurDroit = DigitalInputDevice(capteur_droit)
            self.CapteurDroit.when_activated = self.onChangeD
            self.CapteurDroit.when_deactivated = self.onChangeD
        if capteur_gauche is not None:
            self.CapteurGauche = DigitalInputDevice(capteur_gauche)
            self.CapteurGauche.when_activated = self.onChangeD
            self.CapteurGauche.when_deactivated = self.onChangeD

        self.tailleRoue = 0.5
        # basically will average out if we have both sensors
        if capteur_droit is not None and capteur_gauche is not None:
            self.tailleRoue = self.tailleRoue / 2

        self.LengthLeft = 0  # when 0 on fait le callback
        self.TotalLength = 0  # juste une statistique

        # quand on atteint la longeur voulue, on arrête tout processus
        self.onLengthEnd = self.passFunc
        # a chaque fois que on fait un tours complet
        self.onRoueTournerOnce = self.passFunc

    def passFunc(self):
        pass

    def avancerDistance(self, distance):
        self.LengthLeft = distance

    # chaque changement du capteur de droite
    def onChangeD(self):
        # on enleve la taille de roue (la taille d'entre deux points) a la longueur qui nous reste
        self.LengthLeft -= self.tailleRoue
        self.TotalLength += self.tailleRoue

        # print par pure statistique et pour voir ou on en est
        if self.LengthLeft % 10 == 0 or self.LengthLeft < 1:
            print(self.LengthLeft)

        # s'il reste moins qu zero a la longueur restante pplus la longueur où arrêter
        if self.LengthLeft + self.STOP_LENGTH <= 0:
            self.onLengthEnd()

        # special event apres un tour complet
        #  add .5 par demi fente donc a 10 on a fait 10 fentes, jutulise 9 pour pas que sa start sur l'event et sa aide avec la latence ig?
        if self.TotalLength % 10 == 9:
            self.onRoueTournerOnce()

    # a chaque changement du capteur de gauche
    def onChangeG(self):
        # stub si on veut du code different pour lautre roue
        pass


# main code

# objects
cam = Camera()
rot = encodeurDeRotation(22, 27)
# robot = Robot()

# control variable

mayContinue = True

# hardware functions


def onLengthEndCallback():
    global mayContinue
    mayContinue = False
    print("Distance atteinte, arrêt du robot.")


def onRoueTournerOnceCallback():
    global cam, mayContinue

    if not mayContinue:
        return

    bgrIMG = cam.capturer_image_bgr()
    binIMG = cam.binariser_image_BGR(bgrIMG)

    nbBlobs, _ = cv2.findContours(binIMG, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # trouver le plus grand contour dont l'aire depasse 10000
    SEUIL = 10000
    bigBlob = None
    max_area = 0
    nbBlob = 0
    for r in nbBlobs:
        x, y, w, h = cv2.boundingRect(r)
        area = w * h
        if area > SEUIL and area > max_area:
            max_area = area
            bigBlob = r

        if bigBlob is not None:
            cam.dessiner_rectangle_sur_image(bgrIMG, bigBlob, (0, 255, 0), 2)
            aire, centre = cam.get_dimensions_contour(bigBlob)
            nbBlob += 1
            print(f"Blob trouvé — aire={aire}, centre={centre}")

    bgrIMG = cv2.putText(
        bgrIMG,
        f"Nb blobs: {nbBlob}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        2,
    )
    cv2.imshow("Blob Detection", bgrIMG)

    print("La roue a fait un tour complet.")


# settings

rot.avancerDistance(100)  # 100 -> .5 par fente donc on fait 10 tours avant le call back
rot.onLengthEnd = onLengthEndCallback
rot.onRoueTournerOnce = onRoueTournerOnceCallback

# robot.avancer()

# clean end

while mayContinue:
    key = cv2.waitKeyEx(30)  # attendre 30ms pour l'appui d'une touche
    if key == -1:
        continue
    else:
        key = chr(key)
        if key == "x":
            mayContinue = False
            cv2.destroyAllWindows()


# pour marcher correctement, il faut que le robot soit allumé et que les encodeurs soient branchés aux pins 22 et 27
# ceci nest pas implementer puisque ce netais pas demander et dautre choses peuvent activer les encodeurs
# les encodeures vont arreter automatiquement le robot une fois la distance atteinte via le callback
# on peut rajouter ce code pour que le robot marche aussi :
# ils sont placer dans le code mais commenter pour ne pas causer derreurs si le robot n'est pas la
# les roues doivent etre bouger manuellement pour que les encodeurs detectent le mouvement en ce moment

# from robot import Robot
# robot = Robot()
# robot.avancer()
