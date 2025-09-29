class MapTouches:
    def __init__(self, robot) -> None:
        self.voiture = robot

    def diagoGauche(self):
        self.voiture.diagonale_gauche()

    def diagoDroite(self):
        self.voiture.diagonale_droite()

    def gauche(self):
        self.voiture.tourner_gauche()

    def droite(self):
        self.voiture.tourner_droite()

    def avancer(self):
        self.voiture.avancer()

    def reculer(self):
        self.voiture.reculer()

    def freiner(self):
        self.voiture.arreter()

    def acceler(self):
        self.voiture.modifier_vitesse(0.1)

    def ralentir(self):
        self.voiture.modifier_vitesse(-0.1)

    def shutdown(self):
        self.voiture.shutdown()

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
                return self.acceler()
            case ",":
                return self.ralentir()
            case "x":
                self.shutdown()
                return exit(0)

            case _:
                print("No value for", t)


# ssh pi@192.168.137.229
# cd Documents/pyfile/labs_ses2
# cd C:\Users\emili\OneDrive - Collège Lionel-Groulx\SharedProjects\python
# scp labs_ses2\*.py pi@192.168.137.229:~/Documents/pyfile/
# robot1234
