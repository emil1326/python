import threading
import time
import grovepi  # type: ignore


class scrutteurDigital:
    allowedPorts = [2, 3, 4, 7, 8]
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

    funcOnPress = lambda: None  # ==> fonction si le bouton est presse
    funcOnRelease = lambda: None  # ==> fonction si le bouton est relache
    funcOnHold = lambda: None  # ==> fonction si le bouton est presser

    def __init__(self, port, timeCriticalMode=False, timeCriticalStartTime=0):
        if self.allowedPorts.__contains__(port):
            self.port = port
        else:
            raise ValueError("Port not allowed")

        self.timeCriticalMode = timeCriticalMode
        self.timeCriticalStartTime = timeCriticalStartTime

        grovepi.pinMode(self.port, "INPUT")
        self.check()

    def setFuncOnPress(self, func):
        self.setFuncOnPress = func

    def setFuncOnRelease(self, func):
        self.setFuncOnRelease = func

    def setFuncOnHold(self, func):
        self.setFuncOnHold = func

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
            self.checkThread.join()

        self.checkThread = threading.Thread(
            target=self.checkDigital, args=(self, self.checkWaitTime)
        )
        self.checkThread.start()

    def resetCheckWaitTime(self, checkWaitTime):
        self.checkWaitTime = checkWaitTime
        self.check()

    def checkDigital(self, checkWaitTime):  # => press, release & hold
        isPressed = False

        while not self.endLoop:
            if grovepi.digitalRead(self.port) == 1:
                if not isPressed:
                    isPressed = True
                    if self.verbose:
                        print("Button pressed")
                    self.funcOnPress()
                else:  # button pressed rn
                    if self.verbose:
                        print("Button still pressed")
                    self.funcOnHold()
            else:
                if isPressed:
                    isPressed = False
                    if self.verbose:
                        print("Button released")
                    self.funcOnRelease()

            if self.timeCriticalMode:
                elapsedTime = time.time() - self.timeCriticalStartTime
                sleepTime = max(0, checkWaitTime - (elapsedTime % checkWaitTime))
                time.sleep(sleepTime)
            else:
                time.sleep(checkWaitTime)

            while self.pauseChecks:
                time.sleep(0.1)

        self.endLoop = False  # reset a la fin pour pouvoir relancer le thread
