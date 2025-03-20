import time
from basicPortControlSystem import basicPortControlSystem
from scrutteurHysteresique import scrutteurHysteresique
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog
from lcdController import lcdController

lumHysteresique = scrutteurHysteresique(0)
screen = lcdController(0)

lumHysteresique.waitTimeEntreStates = 2


def up(val):
    print("Est le jour")
    screen.setText("Jour")


def down(val):
    print("Est la nuit")
    screen.setText("Nuit")


def middle(val):
    print("est Middle")
    screen.setText("Millieux")


lumHysteresique.setFuncOnLowerBound(down)
lumHysteresique.setFuncOnUpperBound(up)
lumHysteresique.setFuncOnMiddleBound(middle)


lumHysteresique.Monitor()

input("Finir")

# while True:
#     print(
#         lumHysteresique.currBound,
#         lumHysteresique.getCurrState(),
#         lumHysteresique.currBoundCurrently,
#         lumHysteresique.currValue,
#         time.perf_counter() - lumHysteresique.lastRecordTime,
#         lumHysteresique.waitTimeEntreStates,
#     )
#     # screen.setText(text=(lumHysteresique.getCurrState(), lumHysteresique.currValue))
#     time.sleep(1)

lumHysteresique.StopScrutteur()
