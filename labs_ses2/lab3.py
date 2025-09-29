# Gabriel Pereira Levesque et Emilien
# Laboratoire III | 15 septembre 2025

from gab_robot import Robot
from encodeurDeRotation import encodeurDeRotation

# harware

rot = encodeurDeRotation(False, True)
voiture = Robot()

# harware functions


def endLength():
    voiture.arreter()


# set-up
# comme on le fait par callback
rot.onLengthEnd = endLength

# main

rot.LengthLeft = 100

voiture.avancer(0.5)


input("Finish?")
