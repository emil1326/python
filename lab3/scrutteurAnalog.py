import threading
import time
import grovepi  # type: ignore


class scrutteurAnalog:
    allowedPorts = [0, 1, 2]

    verbose = False

    # port                  #==> port de la pin
    checkThread = None  # ==> thread object
    checkWaitTime = 0.05  # ==> changer sert a rien sans faire check()
    pauseChecks = False  # ==> pause le check
    endLoop = False  # ==> end loop
    timeCriticalMode = False
    # time critical mode, is on on utulise le start time pour avoir le debut de la loop a un moment precis,
    # pour jamais devier, mieux que off pour regulariter mais plus de prosseceur utuliser
    timeCriticalStartTime = 0

    funcOnMin = lambda value: None  # ==> fonction si valeur est en dessous de min
    funcOnMax = lambda value: None  # ==> fonction si valeur est au dessus de max
    funcOnChange = lambda value: None  # ==> fonction a appeler si la valeur change
    funcOnCheck = lambda value: None  # ==> fonction a appeler a chaque check

    valueRange = {"min": 0, "max": 1023}  # default pot range ?

    def __init__(self, port, timeCriticalMode=False, timeCriticalStartTime=0):
        if self.allowedPorts.__contains__(port):
            self.port = port
        else:
            raise ValueError("Port not allowed")

        self.timeCriticalMode = timeCriticalMode
        self.timeCriticalStartTime = timeCriticalStartTime

        grovepi.pinMode(self.port, "INPUT")
        self.check()

    def setFuncOnMin(self, func):
        self.funcOnMin = func

    def setFuncOnMax(self, func):
        self.funcOnMax = func

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
            self.endLoop = True

    def endLoopImmediately(self):  # wait the end else of letting it finish
        self.endLoop = True
        if self.checkThread is not None:
            self.checkThread.join()

    def check(self):
        # if the thread is already running  ==> reset le checkwaittime
        if self.checkThread is not None:
            self.endLoopImmediately()

        self.checkThread = threading.Thread(
            target=self.checkAnalog, args=(self, self.checkWaitTime)
        )
        self.checkThread.start()

    def reSetCheckWaitTime(self, checkWaitTime):
        self.checkWaitTime = checkWaitTime
        self.check()

    def checkAnalog(self, checkWaitTime):  # => min, max, on change, on check
        oldValue = 0

        while not self.endLoop:
            currentValue = grovepi.analogRead(self.port)
            if currentValue <= self.valueRange["min"]:
                self.funcOnMin(currentValue)
                if self.verbose:
                    print("Min value reached:", currentValue)

            elif currentValue >= self.valueRange["max"]:
                self.funcOnMax(currentValue)
                if self.verbose:
                    print("Max value reached:", currentValue)

            else:
                if currentValue != oldValue:
                    self.funcOnChange(currentValue)
                    if self.verbose:
                        print("Value changed:", currentValue)

                self.funcOnCheck(currentValue)
                if self.verbose:
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

        self.endLoop = False  # reset a la fin pour pouvoir relancer le thread
