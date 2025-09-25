from gpiozero import DigitalInputDevice  # type: ignore


class encodeurDeRotation:

    # diametre 6.5cm
    # (6.5 * 3.14159) / 80
    TAILLE_ROUE = 0.5
    STOP_LENGTH = -16.5

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

        self.LengthLeft = 0  # when 0 on fait le callback
        self.TotalLength = 0  # juste une statistique

        self.onLengthEnd = self.passFunc #quand on atteint la longeur voulue, on arrête tout processus 

    def passFun():
        pass
    
    #chaque changement du capteur de droite
    def onChangeD(self):
        #on enleve la taille de roue (la taille d'entre deux points) a la longueur qui nous reste
        self.LengthLeft -= self.TAILLE_ROUE
        self.TotalLength += self.TAILLE_ROUE

        #print par pure statistique et pour voir ou on en est
        if self.LengthLeft % 10 == 0 or self.LengthLeft < 1:
            print(self.LengthLeft)
        
        #s'il reste moins qu zero a la longueur restante pplus la longueur où arrêter
        if self.LengthLeft + self.STOP_LENGTH <= 0:
            self.onLengthEnd()
    
    #a chaque changement du capteur de gauche
    def onChangeG(self):
        #on enleve la taille de roue (la taille d'entre deux points) a la longueur qui nous reste
        self.LengthLeft -= self.TAILLE_ROUE
        self.TotalLength += self.TAILLE_ROUE

        #print par pure statistique et pour voir ou on en est
        if self.LengthLeft % 10 == 0 or self.LengthLeft < 1:
            print(self.LengthLeft)

        #s'il reste moins qu zero a la longueur restante pplus la longueur où arrêter
        if self.LengthLeft + self.STOP_LENGTH <= 0:
            self.onLengthEnd()
