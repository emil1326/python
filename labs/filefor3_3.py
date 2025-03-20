from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog


myDel = basicPortControlSystem(4)
bouton = scrutteurDigital(5)


def change():
    myDel.switchState()


bouton.monitor()

bouton.setFuncOnPress(change)

input("end?")
bouton.endLoop()
myDel.shutDown()
