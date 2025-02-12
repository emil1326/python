import grovepi  # type: ignore
import basicPortControlSystem
import scrutteurDigital


myDel = basicPortControlSystem(4)

myDel.pulse(10, 0.5, 1)
