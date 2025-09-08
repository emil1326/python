from robot import Robot


class MapTouches:
    def __init__(self) -> None:
        self.voiture = Robot()

    def diagoGauche(self):
        self.voiture.turnDL(1)

    def diagoDroite(self):
        self.voiture.turnDR(1)

    def gauche(self):
        self.voiture.turnL(1)

    def droite(self):
        self.voiture.turnR(1)

    def avancer(self):
        self.voiture.avancer(1)

    def reculer(self):
        self.voiture.reculer(1)

    def freiner(self):
        self.voiture.freiner()

    def speedUp(self):
        self.voiture.addMulSpeed(0.1)

    def speedDown(self):
        self.voiture.addMulSpeed(-0.1)

    def map(self, key):
        match (key):
            case ord('q'):
                return self.diagoGauche()
            case ord('w'):
                return self.avancer()
            case ord('e'):
                return self.diagoDroite()
            case ord('a'):
                return self.gauche()
            case ord('s'):
                return self.reculer()
            case ord('d'):
                return self.droite()
            case ord(' '):
                return self.freiner()
            case ord('.'):
                return self.speedUp()
            case ord(','):
                return self.speedDown()
            case ord('x'):
                self.voiture.shutdown()
                return exit(0)

# ssh pi@192.168.137.135
# cd Documents/pyfile/final
# cd C:\Users\emili\OneDrive - Collège Lionel-Groulx\SharedProjects\python
# scp -r labs_ses2 pi@192.168.137.135:~/Documents/pyfile/
# robot1234