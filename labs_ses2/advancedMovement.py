# Gabriel Pereira Levesque & Émilien
# Laboratoire IV | 3 decembre 2025

from labs_ses2.orientation import Orientation
from labs_ses2.gab_lidar import Lidar, Models
from labs_ses2.gab_robot import Robot
from labs_ses2.encodeurDeRotation import encodeurDeRotation
from labs_ses2.rn import RadioNavigation

class AdvancedMovement:    
    def __init__(self):
        self.lidar = Lidar(port="/dev/ttyUSB0", model=Models.X2)
        self.orientation = Orientation()
        self.encodeur = encodeurDeRotation()
        self.radionavigation = RadioNavigation()
        self.robot = Robot(sonar=True, orientation=self.orientation)

