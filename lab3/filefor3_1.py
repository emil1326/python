import grovepi  # type: ignore
from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog


myDel = basicPortControlSystem(4)

myDel.verbose = True

myDel.pulse(10, 0.2, 1)
