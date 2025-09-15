from gpiozero import DigitalInputDevice  # type: ignore


class encodeurDeRotation:

    TAILLE_ROUE = 3.456752389
    STOP_LENGTH = 25

    def __init__(self):
        self.CapteurDroit = DigitalInputDevice(22)
        self.CapteurGauche = DigitalInputDevice(27)

        self.CapteurDroit.when_activated = self.onChangeD
        self.CapteurDroit.when_deactivated = self.onChangeD

        self.CapteurGauche.when_activated = self.onChangeG
        self.CapteurGauche.when_deactivated = self.onChangeG

        self.LengthLeft = 0  # when 0 on fait le callback
        self.TotalLength = 0  # just a stat, no use

        self.onLengthEnd = self.passFunc

    def passFunc(self):
        pass

    def onChangeD(self):

        # pas fait puisque pas besoin live, adder quand meme puisque on a le hardware
        # et vas potentiellement avoir besoin de un >que ou average

        pass

    def onChangeG(self):

        self.LengthLeft -= self.TAILLE_ROUE
        self.TotalLength += self.TAILLE_ROUE

        print(self.LengthLeft)

        if self.LengthLeft + self.STOP_LENGTH <= 0:
            self.onLengthEnd()
