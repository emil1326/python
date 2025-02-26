import threading
import time
import grovepi  # type: ignore
from scrutteurAnalog import scrutteurAnalog


class scrutteurHysteresique:

    verbose = False

    waitTimeEntreStates = 10
    lowerBound = 0.4
    upperBound = 0.6

    # scrutteur = None ==> le scrutteure actif sur cet objet

    # funcOnLowerBound = None
    # funcOnUpperBound = None

    # lastRecordTime ==> last recorded time of a change, used in calcs to know in wich bound we are
    # currBound         ==> ou c mais confirmed
    # currBoundCurrently    ==> ou c mais actually rn

    # currValue

    def __init__(self, port, timeCriticalMode=True, timeCriticalStartTime=0):
        # start un scrutteur analogue avc mode crtical time on de base
        self.scrutteur = scrutteurAnalog(port, timeCriticalMode, timeCriticalStartTime)

        self.lastRecordTime = time.perf_counter()

        self.currBoundCurrently = 0
        self.currBound = None
        self.currValue = -1

        self.funcOnLowerBound = self.passFunc
        self.funcOnUpperBound = self.passFunc

        if self.verbose:
            self.scrutteur.verbose = True
            print("fait un objet scrutteur hysterique")

    def passFunc(self, value):
        pass

    def setFuncOnUpperBound(self, func):
        self.funcOnUpperBound = func

    def setFuncOnLowerBound(self, func):
        self.funcOnLowerBound = func

    def inBetween(self, value):
        timeRN = time.perf_counter()

        if self.currBoundCurrently != 0:
            self.lastRecordTime = timeRN
            self.currBoundCurrently = 0

        if self.lastRecordTime - timeRN >= self.waitTimeEntreStates:
            self.currBound = 0
            self.funcOnUpperBound(value)

    def lowerBoundHit(self, value):
        timeRN = time.perf_counter()

        if self.currBoundCurrently != 1:
            self.lastRecordTime = timeRN
            self.currBoundCurrently = 1

        if self.lastRecordTime - timeRN >= self.waitTimeEntreStates:
            self.currBound = 1
            self.funcOnLowerBound(value)

    def upperBoundHit(self, value):
        timeRN = time.perf_counter()

        if self.currBoundCurrently != 2:
            self.lastRecordTime = timeRN
            self.currBoundCurrently = 2

        if self.lastRecordTime - timeRN >= self.waitTimeEntreStates:
            self.currBound = 2

    def getCurrState(self):
        if self.currBound == 0:
            return None
        return self.currBound

    def Monitor(self):
        self.scrutteur.setMinMax(self.lowerBound, self.upperBound)

        self.scrutteur.setFuncOnMin(self.lowerBoundHit)
        self.scrutteur.setFuncOnMax(self.upperBoundHit)
        self.scrutteur.setFuncOnBetween(self.inBetween)

        self.scrutteur.monitor()
