from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog


myDel = basicPortControlSystem(4)

myDel.verbose = True

myDel.pulseSync(10, 0.2, 1)

myDel.shutDown()
