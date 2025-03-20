import time
from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog


myDel = basicPortControlSystem(4)
bouton = scrutteurDigital(5)
bouton.checkWaitTime = 0.1
bouton.checkWaitTime = 0.01

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
myDel.shutDown()


# 1. oui, si le temps est asser long pour pouvoir faire le click et declique sans que sa soit scrutter,
# personnelement jutulise 0.05 comme valeure par default et sa arrive presque jamais

# 2. a 0.1s, il est rare mais possible de ne pas se faire detecter
# 2. a 0.01s, il est extremement improbable mais toujour possible de ne pas se faire detecter
