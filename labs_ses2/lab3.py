#Gabriel Pereira Levesque et Emilien
#Laboratoire III | 15 septembre 2025

from gab_moteurs import Moteurs
from encodeurDeRotation import encodeurDeRotation

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


input("Finish?")
