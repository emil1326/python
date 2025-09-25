from gpiozero import DigitalInputDevice  # type: ignore


class encodeurDeRotation:

    # diametre 6.5cm
    # (6.5 * 3.14159) / 80
    TAILLE_ROUE = 0.5
    STOP_LENGTH = -16

    def __init__(self, capteur_droit=True, capteur_gauche=True):
        if capteur_droit:
            self.CapteurDroit = DigitalInputDevice(22)
        if capteur_gauche:
            self.CapteurGauche = DigitalInputDevice(27)

        if capteur_droit:
            self.CapteurDroit.when_activated = self.onChangeD        
            self.CapteurDroit.when_deactivated = self.onChangeD
            
        if capteur_gauche:
            self.CapteurGauche.when_activated = self.onChangeG
            self.CapteurGauche.when_deactivated = self.onChangeG

        self.LengthLeft = 0 # when 0 on fait le callback
        self.TotalLength = 0  # juste une statistique

        self.onLengthEnd = self.passFunc

    def passFunc(self):
        pass

    def onChangeD(self):
        
        self.LengthLeft -= self.TAILLE_ROUE
        self.TotalLength += self.TAILLE_ROUE

        if (self.LengthLeft%10==0):
            print(self.LengthLeft)

        if self.LengthLeft + self.STOP_LENGTH <= 0:
            self.onLengthEnd()

    def onChangeG(self):
        self.LengthLeft -= self.TAILLE_ROUE
        self.TotalLength += self.TAILLE_ROUE

        if (self.LengthLeft%10==0):
            print(self.LengthLeft)

        if self.LengthLeft + self.STOP_LENGTH <= 0:
            self.onLengthEnd()
