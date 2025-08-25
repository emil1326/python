from final.robot import Robot


class MapTouches:
    def __init__(self) -> None:
        self.voiture = Robot()

    def diagoGauche(self):
        pass

    def diagoDroite(self):
        pass

    def gauche(self):
        pass

    def droite(self):
        pass

    def avancer(self):
        pass

    def reculer(self):
        pass

    def freiner(self):
        pass
    
    def speedUp(self):
        pass
    
    def speedDown(self):
        

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
            
            case "."
                return self.