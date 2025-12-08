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
    MIN_DIST_Y = 0.10#m
    MAX_DIST_Y = 0.15#m
    MIN_DIST_X = 0.05#m
    MAX_DIST_X = 0.10#m
    
    def __init__(self, port, model, largeur_robot = 0.24, longueur_robot = 0.24) -> None:
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
        
        self.__corridor_x = largeur_robot/2 + 0.05
        self.__corridor_y = largeur_robot/2 + 0.05
    
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
    
    def getPointsObstacle(self):
        points = []
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
                points.append((x_lidar, y_lidar))
            if(points.count()>0):
                return points
            else:
                print('aucuns points trouvé')
                return None
        
        print('un problème est survenu dans le scan')
        return None
    
    def dessinerSurImage(self, img, largeur_image, hauteur_image):
        if self.__lidar is None:
            print("DessinerSurImage_Le lidar n'a pas été initialisé correctement")
            return    
            
        #mise a l'échelle px/metres
        ex = largeur_image/self.RANGE
        ey = hauteur_image/self.RANGE
        
        points = self.getPointsObstacle()
        
        if(points is not None):        
            for (x,y) in points:
                x_pixel = x * ex
                y_pixel = y * ey
                #5. recentrer les points
                x_img = x_pixel + largeur_image/2
                y_img = hauteur_image/2 + y_pixel
                #6. dessiner si possible (x ou y ne dépasse pas le range de limage)
                dessiner = largeur_image > x_img > 0 and hauteur_image > y_img > 0
                #print('dessine sur img', dessiner)
                if dessiner:                        
                    img[int(y_img), int(x_img)] = (255, 255, 255)
                
    def obstacleEnAvant(self, point_x, point_y):
        dans_zone_y = self.MIN_DIST_Y < point_y < self.MAX_DIST_Y
        dans_corridor = abs(point_x) < self.__corridor_x
        
        return dans_zone_y and dans_corridor
    
    def obstacleGauche(self, point_x, min_dist_x, max_dist_x):
        return True
        
