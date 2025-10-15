#gabriel pereira levesque
import gpiozero as gp  # type: ignore

class Moteur:
    IN_A = 0
    IN_B = 1
    PWM = 2

    def __init__(self, port_DOD_A, port_DOD_B, port_PWM):
        # init moteur gauche
        in_a = gp.DigitalOutputDevice(port_DOD_A)
        in_b = gp.DigitalOutputDevice(port_DOD_B)
        pwm = gp.PWMOutputDevice(port_PWM)        
        self.moteur = (in_a, in_b, pwm)
        self.mulSpeed = 1
        self.arreter()

    def avancer(self, vitesse):
        self.moteur[self.PWM].value = vitesse * self.mulSpeed
        self.moteur[self.IN_A].on()
        self.moteur[self.IN_B].off()

    def arreter(self):
        self.moteur[self.PWM].off()
        self.moteur[self.IN_A].off()
        self.moteur[self.IN_B].off()

    def reculer(self, vitesse):
        self.moteur[self.PWM].value = vitesse * self.mulSpeed
        self.moteur[self.IN_A].off()
        self.moteur[self.IN_B].on()

    def addMulSpeed(self, multiplier):
        self.mulSpeed += multiplier
        if self.mulSpeed > 1:
            print("err mul speed", self.mulSpeed)
            self.mulSpeed = 1

        if self.mulSpeed < 0:
            print("err mul speed", self.mulSpeed)
            self.mulSpeed = 0.1

        self.moteur[self.PWM].value = 1 * self.mulSpeed
