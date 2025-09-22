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

    def avancer(
        self, vitesse
    ):
        self.moteur[self.PWM].value = vitesse * self.mulSpeed
        self.moteur[self.IN_A].off()
        self.moteur[self.IN_B].on()

    def arreter(self):
        self.moteur[self.PWM].off()
        self.moteur[self.IN_A].off()
        self.moteur[self.IN_B].off()
        
    def reculer(self, vitesse):
        
        
        pass

    def addMulSpeed(self, multiplier):
        self.mulSpeed += multiplier
        if self.mulSpeed > 1:
            print("err mul speed", self.mulSpeed)
            self.mulSpeed = 1

        if self.mulSpeed < 0:
            print("err mul speed", self.mulSpeed)
            self.mulSpeed = 0.1

        self.moteur[self.PWM].value = 1 * self.mulSpeed   