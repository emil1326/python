import platform
from picamera2 import Picamera2  # type: ignore
import cv2  # type: ignore



class camera:
    LARGEUR = 320
    HAUTEUR = 240

    def __init__(self) -> None:

        picam2 = Picamera2()
        if platform.system() == "Linux":
            print("Workies")
        elif platform.system() == "Windows":
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            return

        # Créer une configuration tout en ajustant le modèle de couleur et la taille de l’image

        config = picam2.create_video_configuration(
            main={"format": "RGB888", "size": (self.LARGEUR, self.HAUTEUR)}
        )
        picam2.configure(config)  # Appliquer la configuration
        picam2.start()  # Démarrer la saisie d’images par la caméra

        image = (
            picam2.capture_array()
        )  # Obtenir l’image de la caméra sous la forme d’un tableau numpy
        
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        

