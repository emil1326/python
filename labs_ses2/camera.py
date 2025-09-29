#gabriel pereira levesque
import platform
import cv2
import numpy as np
from picamera2 import Picamera2

class Camera:
    #constantes
    #resolution de l'image
    LARGEUR = 320
    HAUTEUR = 240
    #limites 
    MIN_HUE = 14
    MAX_HUE = 31
    MIN_SAT = 114
    MAX_SAT = 255
    MIN_VAL = 0
    MAX_VAL = 255
    
    def __init__(self):        
        self.__cam = Picamera2()
        LARGEUR = 320
        HAUTEUR = 240
        config = self.__cam.create_video_configuration(main={"format":"RGB888", "size":(LARGEUR, HAUTEUR)})
        self.__cam.configure(config)
        self.__cam.start()        
    
    #dessine un rectangle sur l'image passée autour d'un contour passé en paramètre 
    def dessiner_rectangle_sur_image(self, image, contour, couleur=(0,0,255), epaisseur=2):
        if contour is None:
            return image
        x, y, l, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x,y), (x+l, y + h), couleur, epaisseur)
    
    #Retourne aire, centre (x, y) d'un contour
    def get_dimensions_contour(self, contour):
        x, y, l, h = cv2.boundingRect(contour)
        aire = l*h
        centre = {"x": x + (l // 2), "y": y + (h // 2)}
        
        return aire, centre
    
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
    def binariser_image(self, image_hsv):
        #définition des bornes
        borne_min = np.array([self.MIN_HUE, self.MIN_SAT, self.MIN_VAL])
        borne_max = np.array([self.MAX_HUE, self.MAX_SAT, self.MAX_VAL])
        
        #création du masque
        masque = cv2.inRange(image_hsv, borne_min, borne_max)
        
        return masque
    
    def convertir_image_bgr2hsv(self, image_bgr):
        image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
        return image_hsv
    
    def capturer_image_bgr(self):
        return self.__cam.capture_array()


    
    
    
    
        
