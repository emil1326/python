class MapTouches:
    def __init__(self, robot=None) -> None:
        if(robot):
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
        if(self.voiture is not None):
            self.voiture.shutdown()

    def map(self, t, voie_libre = True):
        print('mapper_key:', t)
        match t:
            case "q":
                return self.diagoGauche()
            case "w":
                if(voie_libre):
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


# ssh pi@192.168.137.183
# cd Documents/pyfile/labs_ses2
# cd C:\Users\emili\OneDrive - Collège Lionel-Groulx\SharedProjects\python
# scp labs_ses2\*.py pi@192.168.137.183:~/Documents/pyfile/
# scp ./*.py pi@172.20.10.2:~/Documents/pyfile/
# robot1234
