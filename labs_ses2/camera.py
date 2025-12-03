# gabriel pereira levesque
import os
import platform
import cv2  # type: ignore
import numpy as np  # type: ignore


class Camera:
    # constantes
    # resolution de l'image
    LARGEUR = 320
    HAUTEUR = 240
    # limites
    MIN_HUE = 14
    MAX_HUE = 31
    MIN_SAT = 132
    MAX_SAT = 237
    MIN_VAL = 141
    MAX_VAL = 241
    CORRELATION_MIN = 0.3

    ROI = 50

    def __init__(self):
        print("init camera")
        self.__cam = None
        self.__derniere_position_objet = None

        if platform.system() == "Linux":
            from picamera2 import Picamera2  # type: ignore

            self.__cam = Picamera2()
            config = self.__cam.create_video_configuration(
                main={"format": "RGB888", "size": (self.LARGEUR, self.HAUTEUR)}
            )
            self.__cam.configure(config)
            self.__cam.start()
        elif platform.system() == "Windows":
            self.__cam = cv2.VideoCapture(0)
            self.__cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.LARGEUR)
            self.__cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HAUTEUR)
            self.__cam.read()

    #utilisée pour capturer des images d'obstacle ou de voie libre pour le Machine Learning 
    def sauvegarder_image_ml(self, dossier_mere, image, touche, nom_image):
        '''
            dossier_mere = nom du dossier a insérer les images
            image = tableau numpy sorti de cv2
            touche = touche appuyée pour déterminer quel type d'image est capturé (o = obstacle | l = voie libre)
            compteur_image = nom qui doit garantir l'unicité de toutes les images capturées
            retourne void
        '''
        touche_obstacle = "o"
        touche_voie_libre = "l"

        base_path = os.path.join(dossier_mere, "train")
        nom_image = f"{nom_image}.png"

        if touche == touche_voie_libre:
            dossier_cible = os.path.join(base_path, "voie_libre")
        elif touche == touche_obstacle:
            dossier_cible = os.path.join(base_path, "obstacle")
        else:
            return
        os.makedirs(dossier_cible, exist_ok=True)

        chemin_complet = os.path.join(dossier_cible, nom_image)

        try:
            cv2.imwrite(chemin_complet, image)
            print(f"image enregistree dans {dossier_cible}")
        except:
            print("Erreur en sauvegardant :", chemin_complet)

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
    def rechercher_model(self, nom_model, nom_masque):
        model = cv2.imread(nom_model, cv2.IMREAD_GRAYSCALE)
        masque = cv2.imread(nom_masque, cv2.IMREAD_GRAYSCALE)
        
    
        img_bgr = self.capturer_image_bgr()
        img_gray = self.convertir_image_bgr2gray(img_bgr)
        img_cible = img_gray
        ymin = 0
        ymax = self.HAUTEUR
        xmin = 0
        xmax = self.LARGEUR

        if self.__derniere_position_objet is not None:
            ymin = self.__derniere_position_objet["y"] - self.ROI
            ymax = (
                self.__derniere_position_objet["y"] + model.shape[0] + self.ROI
            )  # hauteur
            xmin = self.__derniere_position_objet["x"] - self.ROI
            xmax = (
                self.__derniere_position_objet["x"] + model.shape[1] + self.ROI
            )  # largeur
            cv2.rectangle(img_bgr, (xmin, ymin), (xmax, ymax), (255, 0, 0), 2)

            # bornes dans les dimensions valides
            h, w = img_gray.shape
            ymin = max(0, ymin)
            xmin = max(0, xmin)
            ymax = min(h, ymax)
            xmax = min(w, xmax)

            img_cible = img_gray[ymin:ymax, xmin:xmax]

        res_match = cv2.matchTemplate(
            img_cible, model, cv2.TM_CCOEFF_NORMED, None, masque
        )
        _, max_val, _, max_loc = cv2.minMaxLoc(res_match)

        print(f"max_val = {max_val:.3f} à {max_loc}")

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
        else:
            self.__derniere_position_objet = None
            


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

    def convertir_image_bgr2hsv(self, image_bgr):
        image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        return image_hsv

    # capture et retourne une image (tableau) en source bgr
    def capturer_image_bgr(self):
        if platform.system() == "Linux":
            return self.__cam.capture_array()  # type: ignore
        elif platform.system() == "Windows":
            ret, image = self.__cam.read()  # type: ignore
            return image
    
    def get_derniere_position_objet(self):
        return self.__derniere_position_objet
