import math
import threading
import time
import grovepi  # type: ignore


class scrutteurDigitalDHT:
    allowedPorts = [2, 3, 4, 5, 6]

    verbose = False
    allVerbose = False

    # port                  # ==> port de la pin
    # checkThread = None  # ==> thread object
    # checkWaitTime = 0.5  # ==> changer sert a rien sans faire check(), peu pas etre trop bas pc1q aussi non sa return null
    # pauseChecks = False  # ==> pause le check
    # endLoopFlag = False  # ==> end loop
    # timeCriticalMode = False
    # time critical mode, is on on utulise le start time pour avoir le debut de la loop a un moment precis,
    # pour jamais devier, mieux que off pour regulariter mais plus de prosseceur utuliser
    # timeCriticalStartTime = 0

    # funcOnChange = None  # ==> fonction a appeler si la valeur change
    # funcOnCheck = None  # ==> fonction a appeler a chaque check

    # oldvalue = none #==> prend les value temp/humidity de capteur dht

    def __init__(self, port, timeCriticalMode=False, timeCriticalStartTime=0.0):
        if self.allowedPorts.__contains__(port):
            self.port = port
        else:
            raise ValueError("Port not allowed")

        self.checkThread = None
        self.checkWaitTime = 2
        self.pauseChecks = False
        self.endLoopFlag = False

        self.timeCriticalMode = timeCriticalMode
        self.timeCriticalStartTime = timeCriticalStartTime

        self.funcOnChange = self.passFunc
        self.funcOnCheck = self.passFunc

        self.oldValue = None

        grovepi.pinMode(self.port, "INPUT")

        if self.verbose:
            print("Creer object analog scrutteur")

    def passFunc(self, value):
        pass

    def setFuncOnChange(self, func):
        self.funcOnChange = func

    def setFuncOnCheck(self, func):
        self.funcOnCheck = func

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

    def reSetCheckWaitTimeAndStart(self, checkWaitTime):
        self.checkWaitTime = checkWaitTime
        self.monitor()

    def checkAnalog(self, checkWaitTime):  # => min, max, on change, on check

        while not self.endLoopFlag:

            self.doCheckOnce()

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

    def doCheckOnce(self):
        [temp, humidity] = grovepi.dht(self.port, 0)

        # ==> 0 is blue sensor, 1 is green

        if math.isnan(temp) and math.isnan(humidity):
            print("cant read temp / humidity data on port", self.port)
        else:
            if [temp, humidity] != self.oldValue:
                self.funcOnChange([temp, humidity])
                if self.verbose and self.allVerbose:
                    print("Value changed:", [temp, humidity])

            self.funcOnCheck([temp, humidity])
            if self.verbose and self.allVerbose:
                print("Value checked:", [temp, humidity])

            self.oldValue = [temp, humidity]
