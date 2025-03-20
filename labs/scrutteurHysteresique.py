import threading
import time
import grovepi  # type: ignore
from scrutteurAnalog import scrutteurAnalog


class scrutteurHysteresique:

    verbose = False

    waitTimeEntreStates = 5
    lowerBound = 150
    upperBound = 500

    # scrutteur = None ==> le scrutteure actif sur cet objet

    # funcOnLowerBound = None
    # funcOnUpperBound = None

    # lastRecordTime ==> last recorded time of a change, used in calcs to know in wich bound we are
    # currBound         ==> ou c mais confirmed
    # currBoundCurrently    ==> ou c mais actually rn

    # currValue

    def __init__(self, port, timeCriticalMode=True, timeCriticalStartTime=0.0):
        # start un scrutteur analogue avc mode crtical time on de base
        self.scrutteur = scrutteurAnalog(port, timeCriticalMode, timeCriticalStartTime)

        self.lastRecordTime = time.perf_counter()

        self.currBoundCurrently = 0
        self.currBound = None
        self.currValue = -1

        self.funcOnLowerBound = self.passFunc
        self.funcOnUpperBound = self.passFunc
        self.funcOnMiddleBound = self.passFunc

        if self.verbose:
            self.scrutteur.verbose = True
            print("fait un objet scrutteur hysterique")

    def passFunc(self, value):
        pass

    def setFuncOnUpperBound(self, func):
        self.funcOnUpperBound = func

    def setFuncOnLowerBound(self, func):
        self.funcOnLowerBound = func

    def setFuncOnMiddleBound(self, func):
        self.funcOnMiddleBound = func

    def inBetween(self, value):
        timeRN = time.perf_counter()
        self.currValue = value

        if self.currBoundCurrently == 0:
            self.lastRecordTime = timeRN

        if self.currBoundCurrently != 0:
            self.currBoundCurrently = 0

        # if timeRN - self.lastRecordTime >= self.waitTimeEntreStates:
        self.funcOnMiddleBound(value)

    def lowerBoundHit(self, value):
        timeRN = time.perf_counter()
        self.currValue = value

        if self.currBoundCurrently != 1:
            self.currBoundCurrently = 1

        if (
            timeRN - self.lastRecordTime >= self.waitTimeEntreStates
            and self.currBound != 1
        ):
            self.lastRecordTime = timeRN
            self.currBound = 1
            self.funcOnLowerBound(value)

    def upperBoundHit(self, value):
        timeRN = time.perf_counter()
        self.currValue = value

        if self.currBoundCurrently != 2:
            self.currBoundCurrently = 2

        if (
            timeRN - self.lastRecordTime >= self.waitTimeEntreStates
            and self.currBound != 2
        ):
            self.lastRecordTime = timeRN
            self.currBound = 2
            self.funcOnUpperBound(value)

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

    def StopScrutteur(self):
        self.scrutteur.endLoop()
