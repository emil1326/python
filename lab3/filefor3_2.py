import grovepi # type: ignore
from delController import delController
from scrutteurDigital import scrutteurDigital

myDel = delController(4)
bouton = scrutteurDigital(5)

bouton.setFuncOnPress(lambda: myDel.changeState(1))
bouton.setFuncOnRelease(lambda: myDel.changeState(0))
