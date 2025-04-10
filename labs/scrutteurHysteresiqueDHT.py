import threading
import time
import grovepi  # type: ignore
from ScrutteurAnalogDHT import scrutteurAnalogDHT
from scrutteurAnalog import scrutteurAnalog


class scrutteurHysteresiqueDHT:

    verbose = False

    # waitTimeEntreStates = 5

    # lowerBound = 150
    # upperBound = 500

    # scrutteur = None ==> le scrutteure actif sur cet objet

    # funcOnLowerBound = None
    # funcOnUpperBound = None

    # lastRecordTime ==> last recorded time of a change, used in calcs to know in wich bound we are
    # currBound         ==> ou c mais confirmed
    # currBoundCurrently    ==> ou c mais actually rn

    # currValue
    # always refresh = true => will call funcs when hitting bounds or alwayswhne in the right bound

    def __init__(self, port, timeCriticalMode=True, timeCriticalStartTime=0.0):
        # start un scrutteur analogue avc mode crtical time on de base
        self.scrutteur = scrutteurAnalogDHT(
            port, timeCriticalMode, timeCriticalStartTime
        )

        self.lastRecordTimeTemp = time.perf_counter()
        self.lastRecordTimeHum = self.lastRecordTimeTemp
        self.LastCheckTime = (
            self.lastRecordTimeTemp
        )  # peu pas checker trop souvent => limite les check sur le sensor dht
        self.minCheckTime = 2  # peu pas le faire plus souvent

        self.currBoundCurrentlyTemp = 0 # bound rn
        self.currBoundTemp = None # bound after timings
        self.currValueTemp = -1

        self.currBoundCurrentlyHum = 0 # bound rn 
        self.currBoundHum = None # bound after timings
        self.currValueHum = -1

        self.funcOnLowerBoundTemp = self.passFunc
        self.funcOnUpperBoundTemp = self.passFunc
        self.funcOnMiddleBoundTemp = self.passFunc

        self.funcOnLowerBoundHum = self.passFunc
        self.funcOnUpperBoundHum = self.passFunc
        self.funcOnMiddleBoundHum = self.passFunc

        self.funcOnCheckChild = self.passFunc

        self.waitTimeEntreStatesTemp = 5
        self.waitTimeEntreStatesHum = 5

        self.lowerBoundTemp = 150
        self.upperBoundTemp = 500
        self.lowerBoundHum = 150
        self.upperBoundHum = 500

        self.alwaysRefresh = False

        if self.verbose:
            self.scrutteur.verbose = True
            print("fait un objet scrutteur hysterique")

    def passFunc(self, value):
        pass

    # self funcs

    def setFuncOnUpperBoundTemp(self, func):
        self.funcOnUpperBoundTemp = func

    def setFuncOnLowerBoundTemp(self, func):
        self.funcOnLowerBoundTemp = func

    def setFuncOnMiddleBoundTemp(self, func):
        self.funcOnMiddleBoundTemp = func

    def setFuncOnUpperBoundHum(self, func):
        self.funcOnUpperBoundHum = func

    def setFuncOnLowerBoundHum(self, func):
        self.funcOnLowerBoundHum = func

    def setFuncOnMiddleBoundHum(self, func):
        self.funcOnMiddleBoundHum = func

    def setFuncOnCheckC(self, func):
        self.funcOnCheckChild = func

    # inner funcs

    # temp

    def inBetweenTemp(self, value):
        timeRN = time.perf_counter()
        self.currValueTemp = value

        if self.currBoundCurrentlyTemp == 0:
            self.lastRecordTimeTemp = timeRN

        if self.currBoundCurrentlyTemp != 0:
            self.currBoundCurrentlyTemp = 0

        # if timeRN - self.lastRecordTime >= self.waitTimeEntreStates:
        self.funcOnMiddleBoundTemp(value)

    def lowerBoundHitTemp(self, value):
        timeRN = time.perf_counter()
        self.currValueTemp = value

        if self.currBoundCurrentlyTemp != 1:
            self.currBoundCurrentlyTemp = 1

        if (
            timeRN - self.lastRecordTimeTemp >= self.waitTimeEntreStatesTemp
            and self.currBoundTemp != 1
        ):
            self.lastRecordTimeTemp = timeRN
            self.currBoundTemp = 1
            self.funcOnLowerBoundTemp(value)
        elif (
            timeRN - self.lastRecordTimeTemp >= self.waitTimeEntreStatesTemp
            and self.alwaysRefresh
        ):
            self.lastRecordTimeTemp = timeRN
            self.currBoundTemp = 1
            self.funcOnLowerBoundTemp(value)

    def upperBoundHitTemp(self, value):
        timeRN = time.perf_counter()
        self.currValueTemp = value

        if self.currBoundCurrentlyTemp != 2:
            self.currBoundCurrentlyTemp = 2

        if (
            timeRN - self.lastRecordTimeTemp >= self.waitTimeEntreStatesTemp
            and self.currBoundTemp != 2
        ):
            self.lastRecordTimeTemp = timeRN
            self.currBoundTemp = 2
            self.funcOnUpperBoundTemp(value)
        elif (
            timeRN - self.lastRecordTimeTemp >= self.waitTimeEntreStatesTemp
            and self.alwaysRefresh
        ):
            self.lastRecordTimeTemp = timeRN
            self.currBoundTemp = 2
            self.funcOnUpperBoundTemp(value)

    # hum

    def inBetweenHum(self, value):
        timeRN = time.perf_counter()
        self.currValueHum = value

        if self.currBoundCurrentlyHum == 0:
            self.lastRecordTimeHum = timeRN

        if self.currBoundCurrentlyHum != 0:
            self.currBoundCurrentlyHum = 0

        # if timeRN - self.lastRecordTime >= self.waitTimeEntreStates:
        self.funcOnMiddleBoundHum(value)

    def lowerBoundHitHum(self, value):
        timeRN = time.perf_counter()
        self.currValueHum = value

        if self.currBoundCurrentlyHum != 1:
            self.currBoundCurrentlyHum = 1

        if (
            timeRN - self.lastRecordTimeHum >= self.waitTimeEntreStatesHum
            and self.currBoundHum != 1
        ):
            self.lastRecordTimeHum = timeRN
            self.currBoundHum = 1
            self.funcOnLowerBoundHum(value)
        elif (
            timeRN - self.lastRecordTimeHum >= self.waitTimeEntreStatesHum
            and self.alwaysRefresh
        ):
            self.lastRecordTimeHum = timeRN
            self.currBoundHum = 1
            self.funcOnLowerBoundHum(value)

    def upperBoundHitHum(self, value):
        timeRN = time.perf_counter()
        self.currValueHum = value

        if self.currBoundCurrentlyHum != 2:
            self.currBoundCurrentlyHum = 2

        if (
            timeRN - self.lastRecordTimeHum >= self.waitTimeEntreStatesHum
            and self.currBoundHum != 2
        ): # will only call once
            self.lastRecordTimeHum = timeRN
            self.currBoundHum = 2
            self.funcOnUpperBoundHum(value)
        elif (
            timeRN - self.lastRecordTimeHum >= self.waitTimeEntreStatesHum
            and self.alwaysRefresh
        ): # will call all the times its gets checked & is in this field
            self.lastRecordTimeHum = timeRN
            self.currBoundHum = 2
            self.funcOnUpperBoundHum(value)

    # get states

    def getCurrStateTemp(self):
        if self.currBoundTemp == 0:
            return None
        return self.currBoundTemp

    def getCurrStateHum(self):
        if self.currBoundHum == 0:
            return None
        return self.currBoundHum

    # monitor

    def Monitor(self, startChild=True):
        self.scrutteur.setMinMax(
            self.lowerBoundTemp,
            self.upperBoundTemp,
            self.upperBoundHum,
            self.lowerBoundHum,
        )

        self.scrutteur.setFuncOnMinTemp(self.lowerBoundHitTemp)
        self.scrutteur.setFuncOnMaxTemp(self.upperBoundHitTemp)
        self.scrutteur.setFuncOnBetweenTemp(self.inBetweenTemp)

        self.scrutteur.setFuncOnMinHum(self.lowerBoundHitHum)
        self.scrutteur.setFuncOnMaxHum(self.upperBoundHitHum)
        self.scrutteur.setFuncOnBetweenHum(self.inBetweenHum)
        
        self.scrutteur.setFuncOnCheck(self.funcOnCheckChild)

        if startChild == True:
            self.scrutteur.monitor()

    def StopScrutteur(self):
        self.scrutteur.endLoop()

    def endLoop(self):
        self.scrutteur.endLoop()

    def doCheckOnce(self):
        # need limit checks
        tNow = time.perf_counter()
        if self.minCheckTime < tNow - self.LastCheckTime:
            self.LastCheckTime = tNow
            self.scrutteur.doCheckOnce()
