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

    def avancer(
        self, vitesse, moteur=None
    ):  # moteur = 'g': tourner gauche | 'd': tourner droite | None : avancer en ligne droite
        # moteur gauche
        if moteur == "g" or moteur is None:
            IN1 = 0
            IN2 = 1
            ENA = 2
            self.moteurGauche[ENA].value = vitesse * self.mulSpeed
            self.moteurGauche[ENA].on()
            self.moteurGauche[IN1].on()
            self.moteurGauche[IN2].off()
        # moteur droit
        if moteur == "d" or moteur is None:
            IN3 = 0
            IN4 = 1
            ENB = 2
            self.moteurDroit[ENB].value = vitesse * self.mulSpeed
            self.moteurDroit[ENB].on()
            self.moteurDroit[IN3].on()
            self.moteurDroit[IN4].off()

    def diagonale_gauche(self, vitesse):
        # moteur gauche a la moitie de la vitesse
        IN1 = 0
        IN2 = 1
        ENA = 2
        self.moteurGauche[ENA].value = vitesse / 2 * self.mulSpeed
        self.moteurGauche[ENA].on()
        self.moteurGauche[IN1].on()
        self.moteurGauche[IN2].off()
        # moteur droit a pleine vitesse
        IN3 = 0
        IN4 = 1
        ENB = 2
        self.moteurDroit[ENB].value = vitesse * self.mulSpeed
        self.moteurDroit[ENB].on()
        self.moteurDroit[IN3].on()
        self.moteurDroit[IN4].off()

    def diagonale_droite(self, vitesse):
        # moteur gauche a pleine vitesse
        IN1 = 0
        IN2 = 1
        ENA = 2
        self.moteurGauche[ENA].value = vitesse * self.mulSpeed
        self.moteurGauche[ENA].on()
        self.moteurGauche[IN1].on()
        self.moteurGauche[IN2].off()
        # moteur droit a la moitie de la vitesse
        IN3 = 0
        IN4 = 1
        ENB = 2
        self.moteurDroit[ENB].value = vitesse / 2 * self.mulSpeed
        self.moteurDroit[ENB].on()
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
