import time
import grovepi  # type: ignore
from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog


myDel = basicPortControlSystem(4)
bouton = scrutteurDigital(5)

bouton.verbose = True


def on():
    myDel.changeState(1)


def off():
    myDel.changeState(0)


bouton.setFuncOnPress(on)
bouton.setFuncOnRelease(off)

bouton.monitor()

input("finir?")
bouton.endLoop()
