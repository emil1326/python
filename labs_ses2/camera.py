#gabriel pereira levesque
import platform
import cv2

class Camera:
    LARGEUR = 320
    HAUTEUR = 240
    MIN_HUE = 0
    MAX_HUE = 179
    MAX_SAT = 100
    MIN_SAT = 0
    
    
    def __init__(self):
        from picamera2 import Picamera2
        self.__cam = Picamera2()
        config = picam2.create_video_configuration(main={"format":"RGB888", "size":(LARGEUR, HAUTEUR)})
        self.__cam.configure(config)
        self.__cam.start()
        
        self.__image_array = self.__cam.capture_array()
    
    
    def __convertir_image_hsv(self, image):
        cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    def capturer_image(self):
        self.__image_array = self.__cam.capture_array()
        return self.__image_array


    
    
    
    
        