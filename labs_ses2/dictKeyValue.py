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

    def map(self, t):
        match (t):
            case 'q':
                return self.diagoGauche()
            case 'w':
                return self.avancer()
            case 'e':
                return self.diagoDroite()
            case 'a':
                return self.gauche()
            case 's':
                return self.reculer()
            case 'd':
                return self.droite()
            case ' ':
                return self.freiner()

            case '.':
                return self.speedUp()
            case ',':
                return self.speedDown()
            case 'x':
                self.voiture.shutdown()
                return exit(0)


# ssh pi@192.168.137.229
# cd Documents/pyfile/labs_ses2
# cd C:\Users\emili\OneDrive - Collège Lionel-Groulx\SharedProjects\python
# scp -r labs_ses2 pi@192.168.137.229:~/Documents/pyfile/
# robot1234
