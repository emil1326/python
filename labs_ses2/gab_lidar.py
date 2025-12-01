import ydlidar # type: ignore
import enum
from math import (sin, cos)
import cv2

class Models(enum.Enum):
    X2 = 1
    X4 = 2

class Lidar:  
    RANGE = 3 #metres de range parce que le max (8m ou 10m) serait trop
    SCAN = None
    
    def __init__(self, port, model) -> None:
        if model == Models.X2:
            self.__BAUD = 115200
            self.__SAMPLE_RATE = 4
            self.__SCAN_FREQ = 6.0
            self.__SINGLE_CHANNEL = True
            self.__LIDAR_TYPE = ydlidar.TYPE_TOF
        elif model == Models.X4:
            self.__BAUD = 128000 
            self.__SAMPLE_RATE = 8
            self.__SCAN_FREQ = 7.0
            self.__SINGLE_CHANNEL = False
            self.__LIDAR_TYPE = ydlidar.TYPE_TRIANGLE
        else:
            raise ValueError('Veuillez entrer un model contenu dans lenum Models')
        
        ydlidar.os_init()
        self.LASER = ydlidar.CYdLidar()
        self.LASER.setlidaropt(ydlidar.LidarPropSerialPort, port)
        self.LASER.setlidaropt(ydlidar.LidarPropSerialBaudrate, self.__BAUD)
        self.LASER.setlidaropt(ydlidar.LidarPropLidarType, self.__LIDAR_TYPE)
        self.LASER.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
        self.LASER.setlidaropt(ydlidar.LidarPropSampleRate, self.__SAMPLE_RATE)
        self.LASER.setlidaropt(ydlidar.LidarPropScanFrequency, self.__SCAN_FREQ)
        self.LASER.setlidaropt(ydlidar.LidarPropSingleChannel, self.__SINGLE_CHANNEL)
        self.__lidar = self.LASER
    
    def demarrer(self):
        '''
            démarre le lidar et routourne True. Si un problème survient, retourne False
        '''
        if self.__lidar is None:
            print("Demarrer_Le lidar n'a pas été initialisé correctement")
            return False
        
        ret = self.__lidar.initialize()
        if(ret):
            self.__ret = self.__lidar.turnOn()
            return True
        else:
            print("Demarrer_Le lidar n'a pas reussi a s'ouvrir")        
            return False
    
    def arreter(self):
        if self.__lidar is None:
            print("Arreter_Le lidar n'a pas été initialisé correctement")
            return
        
        self.__lidar.turnOff()
        self.__lidar.disconnecting()
    
    def dessinerSurImage(self, img, largeur_image, hauteur_image):
        if self.__lidar is None:
            print("DessinerSurImage_Le lidar n'a pas été initialisé correctement")
            return    
            
        #mise a l'échelle px/metres
        ex = largeur_image/self.RANGE
        ey = hauteur_image/self.RANGE
        
        #1. scan
        scan = ydlidar.LaserScan()
        r = self.__lidar.doProcessSimple(scan)
        if r:
            for point in scan.points:
                #2. get l'angle et distance
                a = point.angle
                d = point.range
                #si la distance depasse le range, pas besoin de le calculer
                if(d > self.RANGE):
                    continue
                #3. get x et y grace a l'angle en radian
                x_lidar = -d*sin(a)
                y_lidar = d*cos(a)
                
                x_pixel = x_lidar * ex
                y_pixel = y_lidar * ey
                #5. recentrer les points
                x_img = x_pixel + largeur_image/2
                y_img = hauteur_image/2 + y_pixel
                #6. dessiner si possible (x ou y ne dépasse pas le range de limage)
                dessiner = largeur_image > x_img > 0 and hauteur_image > y_img > 0
                #print('dessine sur img', dessiner)
                if dessiner:                        
                    img[int(y_img), int(x_img)] = (255, 255, 255)
                
        
