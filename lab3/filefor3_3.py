import grovepi # type: ignore
import delController
import scrutteurDigital


myDel = delController(4)
bouton = scrutteurDigital(5)

bouton.setFuncOnPress(lambda: myDel.switchState())
