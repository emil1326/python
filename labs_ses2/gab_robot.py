from gab_moteurs import Moteur
from sonar import Sonar
from dels import Dels

class Robot:
    
    def __init__(self):
        self.__dels = Dels()
        self.__sonarG = Sonar(25, 8)
        self.__sonarD = Sonar(20, 21)
        self.__moteur
        