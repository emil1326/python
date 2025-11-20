import ydlidar
import enum

class Models(Enum):
    X2 = 1
    X4 = 2

class Lidar:  
    #fais pas la surprise jai enlevé lidée de la deuxieme classe parce que dans le lab6 ca nous aide pas plus, pourquoi ca nous aiderait dans celui-ci?
    
    RANGE = 3 #metres de range parce que le max (8m ou 10m) serait trop
    
    def __init__(self, port, model) -> None:
        self.__lidar = None
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
        self.__lidar = ydlidar.CYdLidar()
        self.__lidar.setlidaropt(ydlidar.LidarPropSerialPort, port)
        self.__lidar.setlidaropt(ydlidar.LidarPropSerialBaudrate, self.__BAUD)
        self.__lidar.setlidaropt(ydlidar.LidarPropLidarType, self.__LIDAR_TYPE)
        self.__lidar.setlidaropt(ydlidar.LidarPropDeviceType, self.__LIDAR_TYPE)
        self.__lidar.setlidaropt(ydlidar.LidarPropSampleRate, self.__SAMPLE_RATE)
        self.__lidar.setlidaropt(ydlidar.LidarPropScanFrequency, self.__SCAN_FREQ)
        self.__lidar.setlidaropt(ydlidar.LidarPropSingleChannel, self.__SINGLE_CHANNEL)
    
    def demarrer(self):
        '''
            demarre le lidar. Si un problème survient, une ConnectionError est levée
        '''
        ret = self.__lidar.initialize()
        if(ret):
            self.__ret = self.__lidar.turnOn()
        else:
            raise ConnectionError("Le lidar n'a pas reussi a s'ouvir")        
    
    def arreter(self):
        self.__lidar.turnOff();
        self.__lidar.disconnecting();
    
    def dessinerSurImage(self, img):
        #1. scan
        scan = ydlidar.LaserScan()
        while self.__ret and ydlidar.os_isOk():
            r = self.__lidar.doProcessSimple(scan)
                          
            #2. get l'angle 
        #3. get x et y grace a l'angle
        #4. 
        if not lidar.initialize():
            pass
        if not lidar.turnOn():
            pass
