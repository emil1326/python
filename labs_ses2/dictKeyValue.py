from final.robot import Robot
from final.moteur import Moteur


class MapTouches:
    def __init__(self) -> None:
        self.voiture = Robot()

    def diagoGauche(self):
        Robot.turnDL(Robot, 1)

    def diagoDroite(self):
        Robot.turnDR(Robot, 1)

    def gauche(self):
        Robot.turnL(Robot, 1)

    def droite(self):
        Robot.turnR(Robot, 1)

    def avancer(self):
        Robot.avancer(Robot, 1)

    def reculer(self):
        Robot.reculer(Robot, 1)

    def freiner(self):
        Robot.freiner(Robot, 1)

    def speedUp(self):
        Robot.setM

    def speedDown(self):
        pass

    def map(self, t):
        match (t):
            case "q":
                return self.diagoGauche()
            case "w":
                return self.avancer()
            case "e":
                return self.diagoDroite()
            case "a":
                return self.gauche()
            case "s":
                return self.reculer()
            case "d":
                return self.droite()
            case " ":
                return self.freiner()

            case ".":
                return self.speedUp()
            case ",":
                return self.speedDown()
            case 'x':
                self.voiture.shutdown()
                return exit(0)
