#gabriel pereira levesque
import platform
import cv2
import numpy as np

class Camera:
    #constantes
    #resolution de l'image
    LARGEUR = 320
    HAUTEUR = 240
    #limites 
    MIN_HUE = 20
    MAX_HUE = 30
    MIN_SAT = 50
    MAX_SAT = 255
    MIN_VAL = 30
    MAX_VAL = 255
    
    def __init__(self):
        from picamera2 import Picamera2
        self.__cam = Picamera2()
        config = picam2.create_video_configuration(main={"format":"RGB888", "size":(LARGEUR, HAUTEUR)})
        self.__cam.configure(config)
        self.__cam.start()
        
        self.__image_array = self.__cam.capture_array()
    
    def dessiner_rectangle_sur_image(self, image, contour, couleur=(0,0,255), epaisseur=2):
        if contour is None:
            return image
        x, y, l, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x,y), (x+l, y + h), couleur, epaisseur)
    
    def get_dimensions_contour(self, contour):
        x, y, l, h = cv2.boundingRect(contour)
        aire = l*h
        centre = {"x": x + (l // 2), "y": y + (h // 2)}
        
        return {"aire":aire, "centre": centre}
    
    #prend une image binarise et retourne les coordonnees {centre, aire} du plus gros blob
    def get_plus_gros_contour(self, image_bin):
        plus_gros_contour = None
        max_aire = 0
        
        contours, _ = cv2.findContours(image_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        for c in contours:
            x, y, l, h = cv2.boundingRect(c)
            aire = l*h
            if aire > max_aire:
                max_aire = aire
                plus_gros_contour = c                
        
        return plus_gros_contour 
    
    #prend une image hsv et la binarise
    def __binariser_image(self, image_hsv):
        #définition des bornes
        borne_min = np.array([self.MIN_HUE, self.MIN_SAT, self.MIN_VAL])
        borne_max = np.array([self.MAX_HUE, self.MAX_SAT, self.MAX_VAL])
        
        #création du masque
        masque = cv2.inRange(image_hsv, borne_min, borne_max)
        
        return masque
    
    def __convertir_image_hsv(self, image):
        image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        return image_hsv
    
    def capturer_image(self):
        return self.__cam.capture_array()


    
    
    
    
        
