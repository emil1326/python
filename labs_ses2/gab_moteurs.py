import gpiozero as gp  # type: ignore


class Moteur:
    IN_A = 0
    IN_B = 1
    PWM = 2
    
    def __init__(self, port_DOD_A, port_DOD_B, port_PWM):
        # init moteur gauche
        in_a = gp.DigitalOutputDevice(6)
        in_b = gp.DigitalOutputDevice(5)
        pwm = gp.PWMOutputDevice(13)
        self.moteur = (in_a, in_b, pwm)
       

        self.mulSpeed = 1

    def __rien(self):
        
        self.moteur[PWM].value = 0
        self.moteur[PWM].on()
        self.moteur[IN_A].off()
        self.moteur[IN_B].off()

    def avancer(
        self, vitesse, direction=None
    ):  # direction = 'g': tourner gauche | 'd': tourner droite | None : avancer en ligne droite
        self.moteurGauche[PWM].value = vitesse * self.mulSpeed
        self.moteurGauche[IN_A].off()
        self.moteurGauche[IN_B].on()

    #TODO mettre cette logique dans robot, avec mulspeed changeable par moteur, on peut diviser dans robot
    def diagonale_gauche(self, vitesse):
        self.__rien()
        # moteur gauche a la moitie de la vitesse
        IN1 = 0
        IN2 = 1
        ENA = 2
        self.moteurGauche[ENA].value = vitesse * self.mulSpeed / 4
        self.moteurGauche[IN1].on()
        self.moteurGauche[IN2].off()
        # moteur droit a pleine vitesse
        IN3 = 0
        IN4 = 1
        ENB = 2
        self.moteurDroit[ENB].value = vitesse * self.mulSpeed
        self.moteurDroit[IN3].on()
        self.moteurDroit[IN4].off()
        
    #TODO mettre cette logique dans robot, avec mulspeed changeable par moteur, on peut diviser dans robot
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
        self.moteurDroit[ENB].value = vitesse  * self.mulSpeed / 4
        self.moteurDroit[IN3].on()
        self.moteurDroit[IN4].off()

    #TODO remplacer pour faire reculer un moteur, mettre la logique incluant les deux moteurs dans robot
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

    #TODO remplacer pour faire arreter un moteur, mettre la logique pour arreter les deux dans robot
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

    #TODO remplacer pour ajouter de la vit a un moteur, mettre la logique pour ajouter aux deux dans robot
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