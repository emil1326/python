from time import sleep
import grovepi  # type: ignore
from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital


# declare hardware

lumiere1 = basicPortControlSystem(2)
lumiere2 = basicPortControlSystem(4)

# utulise time critical pour sassurer que les 2 ne peuve pas sexecutter en meme temps avc .5 decart
# peu etre plus bas +- .0028 s d'experience au minimum pour faire comme si sa se passait en meme temps
# 2 scrutteur sur le mem pas super mais sa marche => sur un fau port, rien a checker juste besoin des loops

# peut timer 5 sur 0, .01, .02, .03, .04
# plus faut increase le base wait speed de .05 ou reduire la difference de timing, peut aller aussi bas que .005 safely donc bc de channels de libre

# comme lock mais plus soft, lock ferait le meme decalage mais plus petit

bouton = scrutteurDigital(3, True, 0.02)
boutonL1 = scrutteurDigital(8, True, 0)
boutonL2 = scrutteurDigital(8, True, 0.01)

# test hardware

sleep(0.5)

lumiere1.pulseAsync(2, 0.1, 0.2)
sleep(0.01)
lumiere2.pulseSync(2, 0.1, 0.2)

sleep(0.5)

# declare hardware functions


def onCheckRedoL1():
    lumiere1.pulseSync(1, 1, 0)  # no outtime puisque juste 1 fois


def onCheckRedoL2():
    lumiere2.pulseSync(1, 2, 0)


def pressedButtonStop():
    bouton.endLoop()
    boutonL1.endLoop()
    boutonL2.endLoop()
    lumiere1.shutDown()
    lumiere2.shutDown()

    print("can end safely")


# start monitoring

bouton.monitor()
boutonL1.resetCheckWaitTime(2)
boutonL2.resetCheckWaitTime(4)

# link hardware functions

bouton.setFuncOnPress(pressedButtonStop)
boutonL1.setFuncOnCheck(onCheckRedoL1)
boutonL2.setFuncOnCheck(onCheckRedoL2)

# wait for end

input("finish?")

# finish

bouton.endLoop()
boutonL1.endLoop()
boutonL2.endLoop()
bouton.endLoopImmediately()
boutonL1.endLoopImmediately()
boutonL2.endLoopImmediately()
lumiere1.shutDown()
lumiere2.shutDown()
