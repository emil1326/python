import threading
import time
import grovepi  # type: ignore


class scrutteurAnalog:
    allowedPorts = [0, 1, 2]

    verbose = False
    allVerbose = False

    steps = None  # ==> espacement entre les valeures analogiques possible

    # port                  # ==> port de la pin
    # checkThread = None  # ==> thread object
    # checkWaitTime = 0.05  # ==> changer sert a rien sans faire check()
    # pauseChecks = False  # ==> pause le check
    # endLoopFlag = False  # ==> end loop
    # timeCriticalMode = False
    # time critical mode, is on on utulise le start time pour avoir le debut de la loop a un moment precis,
    # pour jamais devier, mieux que off pour regulariter mais plus de prosseceur utuliser
    # timeCriticalStartTime = 0

    # funcOnMin = None  # ==> fonction si valeur est en dessous de min
    # funcOnMax = None  # ==> fonction si valeur est au dessus de max
    # funcOnChange = None  # ==> fonction a appeler si la valeur change
    # funcOnCheck = None  # ==> fonction a appeler a chaque check
    # funcOnBetween = none

    # valueRange = {"min": 0, "max": 1023}  # default pot range ?

    def __init__(self, port, timeCriticalMode=False, timeCriticalStartTime=0):
        if self.allowedPorts.__contains__(port):
            self.port = port
        else:
            raise ValueError("Port not allowed")

        self.checkThread = None
        self.checkWaitTime = 0.05
        self.pauseChecks = False
        self.endLoopFlag = False

        self.timeCriticalMode = timeCriticalMode
        self.timeCriticalStartTime = timeCriticalStartTime

        self.valueRange = {"min": 0, "max": 1023}

        self.funcOnMin = self.passFunc
        self.funcOnMax = self.passFunc
        self.funcOnChange = self.passFunc
        self.funcOnCheck = self.passFunc
        self.funcOnBetween = self.passFunc

        grovepi.pinMode(self.port, "INPUT")

        if self.verbose:
            print("Creer object analog scrutteur")

    def passFunc(self, value):
        pass

    def setFuncOnMin(self, func):
        self.funcOnMin = func

    def setFuncOnMax(self, func):
        self.funcOnMax = func

    def setFuncOnBetween(self, func):
        self.funcOnBetween = func

    def setFuncOnChange(self, func):
        self.funcOnChange = func

    def setFuncOnCheck(self, func):
        self.funcOnCheck = func

    def setMin(self, min_val):
        self.valueRange["min"] = min_val

    def setMax(self, max_val):
        self.valueRange["max"] = max_val

    def setMinMax(self, min_val, max_val):
        self.setMin(min_val)
        self.setMax(max_val)

    def endLoop(self):
        if self.checkThread is not None:
            self.endLoopFlag = True

    def endLoopImmediately(self):  # wait the end else of letting it finish
        self.endLoopFlag = True
        if self.checkThread is not None:
            self.checkThread.join()

    def monitor(self):
        # if the thread is already running  ==> reset le checkwaittime
        if self.checkThread is not None:
            self.endLoopImmediately()

        self.checkThread = threading.Thread(
            target=self.checkAnalog, args=(self.checkWaitTime,)
        )
        self.checkThread.start()

    def reSetCheckWaitTime(self, checkWaitTime):
        self.checkWaitTime = checkWaitTime
        self.monitor()

    def __getStepped(self, steps, value):
        val = value / steps
        val = round(val)
        val = val * steps

        return val

    def checkAnalog(self, checkWaitTime):  # => min, max, on change, on check
        oldValue = 0

        while not self.endLoopFlag:
            currentValue = grovepi.analogRead(self.port)

            if self.steps != None:
                currentValue = self.__getStepped(self.steps, currentValue)

            #

            if currentValue <= self.valueRange["min"]:
                self.funcOnMin(currentValue)
                if self.verbose:
                    print("Min value reached:", currentValue)

            elif currentValue >= self.valueRange["max"]:
                self.funcOnMax(currentValue)
                if self.verbose:
                    print("Max value reached:", currentValue)
            else:
                self.funcOnBetween
                if self.verbose:
                    print("Is in between value:", currentValue)

            #

            if currentValue != oldValue:
                self.funcOnChange(currentValue)
                if self.verbose and self.allVerbose:
                    print("Value changed:", currentValue)

            self.funcOnCheck(currentValue)
            if self.verbose and self.allVerbose:
                print("Value checked:", currentValue)

            oldValue = currentValue

            if self.timeCriticalMode:
                elapsedTime = time.time() - self.timeCriticalStartTime
                sleepTime = max(0, checkWaitTime - (elapsedTime % checkWaitTime))
                time.sleep(sleepTime)
            else:
                time.sleep(checkWaitTime)
            # check wait time ici pour empecher les changements externe

            while self.pauseChecks:
                time.sleep(0.1)

        self.endLoopFlag = False  # reset a la fin pour pouvoir relancer le thread
