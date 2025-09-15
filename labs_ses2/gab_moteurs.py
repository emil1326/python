import gpiozero as gp  # type: ignore


class Moteurs:
    def __init__(self):
        # init moteur gauche
        IN1 = gp.DigitalOutputDevice(6)
        IN2 = gp.DigitalOutputDevice(5)
        ENA = gp.PWMOutputDevice(13)
        self.moteurGauche = (IN1, IN2, ENA)
        # init moteur droit
        IN3 = gp.DigitalOutputDevice(15)
        IN4 = gp.DigitalOutputDevice(14)
        ENB = gp.PWMOutputDevice(18)
        self.moteurDroit = (IN3, IN4, ENB)

        self.mulSpeed = 1

    def __rien(self):
        IN1 = 0
        IN2 = 1
        ENA = 2
        IN3 = 0
        IN4 = 1
        ENB = 2
        self.moteurGauche[ENA].value = 0
        self.moteurGauche[ENA].on()
        self.moteurGauche[IN1].off()
        self.moteurGauche[IN2].off()
        # moteur droit
        self.moteurDroit[ENB].value = 0
        self.moteurDroit[ENB].on()
        self.moteurDroit[IN3].off()
        self.moteurDroit[IN4].off()

    def avancer(
        self, vitesse, direction=None
    ):  # direction = 'g': tourner gauche | 'd': tourner droite | None : avancer en ligne droite

        IN1 = 0
        IN2 = 1
        ENA = 2
        IN3 = 0
        IN4 = 1
        ENB = 2

        if direction == "g":  # reverse moteur g pour trouner a gauche
            self.moteurGauche[ENA].value = vitesse * self.mulSpeed
            self.moteurGauche[IN1].off()
            self.moteurGauche[IN2].on()
        if direction == "d":  # reverse moteur droit pour tourner a droite
            self.moteurDroit[ENB].value = vitesse * self.mulSpeed
            self.moteurDroit[IN3].off()
            self.moteurDroit[IN4].on()

        if (
            direction == "d" or direction is None
        ):  # avancer avec moteur gauche pour trouner a droite

            self.moteurGauche[ENA].value = vitesse * self.mulSpeed
            self.moteurGauche[IN1].on()
            self.moteurGauche[IN2].off()
        # moteur droit
        if (
            direction == "g" or direction is None
        ):  # avacer avec moteur droit pour trouner a gauche

            self.moteurDroit[ENB].value = vitesse * self.mulSpeed
            self.moteurDroit[IN3].on()
            self.moteurDroit[IN4].off()

    def diagonale_gauche(self, vitesse):
        self.__rien()
        # moteur gauche a la moitie de la vitesse
        IN1 = 0
        IN2 = 1
        ENA = 2
        self.moteurGauche[ENA].value = vitesse * self.mulSpeed / 2
        self.moteurGauche[IN1].on()
        self.moteurGauche[IN2].off()
        # moteur droit a pleine vitesse
        IN3 = 0
        IN4 = 1
        ENB = 2
        self.moteurDroit[ENB].value = vitesse * self.mulSpeed
        self.moteurDroit[IN3].on()
        self.moteurDroit[IN4].off()

    def diagonale_droite(self, vitesse):
        self.__rien()
        # moteur gauche a pleine vitesse
        IN1 = 0
        IN2 = 1
        ENA = 2
        self.moteurGauche[ENA].value = vitesse * self.mulSpeed
        self.moteurGauche[IN1].on()
        self.moteurGauche[IN2].off()
        # moteur droit a la moitie de la vitesse
        IN3 = 0
        IN4 = 1
        ENB = 2
        self.moteurDroit[ENB].value = vitesse  * self.mulSpeed / 2
        self.moteurDroit[IN3].on()
        self.moteurDroit[IN4].off()

    def reculer(self, vitesse):
        # moteur gauche
        IN1 = 0
        IN2 = 1
        ENA = 2
        self.moteurGauche[ENA].value = vitesse * self.mulSpeed
        self.moteurGauche[ENA].on()
        self.moteurGauche[IN1].off()
        self.moteurGauche[IN2].on()
        # moteur droit
        IN3 = 0
        IN4 = 1
        ENB = 2
        self.moteurDroit[ENB].value = vitesse * self.mulSpeed
        self.moteurDroit[ENB].on()
        self.moteurDroit[IN3].off()
        self.moteurDroit[IN4].on()

    def arreter(self):
        # moteur gauche
        IN1 = 0
        IN2 = 1
        ENA = 2
        self.moteurGauche[ENA].off()
        self.moteurGauche[IN1].off()
        self.moteurGauche[IN2].off()
        # moteur droit
        IN3 = 0
        IN4 = 1
        ENB = 2
        self.moteurDroit[ENB].off()
        self.moteurDroit[IN3].off()
        self.moteurDroit[IN4].off()

    def addMulSpeed(self, multiplier):
        self.mulSpeed += multiplier
        if self.mulSpeed > 1:
            print("err mul speed", self.mulSpeed)
            self.mulSpeed = 1

        if self.mulSpeed < 0:
            print("err mul speed", self.mulSpeed)
            self.mulSpeed = 0.1

        self.moteurDroit[2].value = 1 * self.mulSpeed       
        self.moteurGauche[2].value = 1 * self.mulSpeed