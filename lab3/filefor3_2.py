import grovepi # type: ignore
import basicPortControlSystem
import scrutteurDigital

myDel = basicPortControlSystem(4)
bouton = scrutteurDigital(5)

bouton.setFuncOnPress(lambda: myDel.changeState(1))
bouton.setFuncOnRelease(lambda: myDel.changeState(0))
