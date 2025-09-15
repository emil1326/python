from labs_ses2.gab_moteurs import Moteurs
from labs_ses2.encodeurDeRotation import encodeurDeRotation

# harware

rot = encodeurDeRotation()
voiture = Moteurs()

# harware functions


def endLength():
    voiture.arreter()
    pass


# set-up

rot.onLengthEnd = endLength

# main

rot.LengthLeft = 100

voiture.avancer(1)
