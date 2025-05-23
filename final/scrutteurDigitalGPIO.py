import threading
import time
from gpiozero import DigitalInputDevice  # type: ignore


class scrutteurDigitalGPIO:
    allowedPorts = [
        2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
        18, 19, 20, 21, 22, 23, 24, 25, 26, 27
    ]
    
    verbose = False

    # port                  #==> port de la pin
    # checkThread = None  # ==> thread object
    # checkWaitTime = 0.05  # ==> changer sert a rien sans faire check()
    # pauseChecks = False  # ==> pause le check
    # endLoopFlag = False  # ==> end loop
    # timeCriticalMode = False
    # time critical mode, is on on utulise le start time pour avoir le debut de la loop a un moment precis,
    # pour jamais devier, mieux que off pour regulariter mais plus de prosseceur utuliser
    # timeCriticalStartTime = 0

    # funcOnPress = None  # ==> fonction si le bouton est presse
    # funcOnRelease = None  # ==> fonction si le bouton est relache
    # funcOnHold = None  # ==> fonction si le bouton est presser
    # funcOnCheck = None

    # isPressed = false # ==> forLogic is pressed

    def __init__(self, port, timeCriticalMode=False, timeCriticalStartTime=0.0):
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

        self.funcOnPress = self.passFunc
        self.funcOnRelease = self.passFunc
        self.funcOnHold = self.passFunc
        self.funcOnCheck = self.passFunc

        self.isPressed = False

        self.device = DigitalInputDevice(self.port, pull_up=True)

        if self.verbose:
            print("Creer object digi scrutteur")

    def passFunc(self):
        pass

    def setFuncOnPress(self, func):
        self.funcOnPress = func

        if self.verbose:
            print("setted function", func, "on press")

    def setFuncOnRelease(self, func):
        self.funcOnRelease = func

        if self.verbose:
            print("setted function", func, "on release")

    def setFuncOnHold(self, func):
        self.funcOnHold = func

        if self.verbose:
            print("setted function", func, "on hold")

    def setFuncOnCheck(self, func):
        self.funcOnCheck = func

        if self.verbose:
            print("setted function", func, "on check")

    def endLoop(self):
        if self.checkThread is not None:
            self.endLoopFlag = True

            if self.verbose:
                print("Ended loop pour digi scrutteur")
        if self.verbose:
            print("tryied to change flag")

    def endLoopImmediately(self):  # wait the end else of letting it finish
        self.endLoopFlag = True
        if self.checkThread is not None:
            self.checkThread.join()

            if self.verbose:
                print("Ended loop Immediately pour digi scrutteur")

    def monitor(self):
        # if the thread is already running  ==> reset le checkwaittime
        if self.checkThread is not None:
            self.checkThread.join()

        self.endLoopFlag = False

        self.checkThread = threading.Thread(
            target=self.checkDigital, args=(self.checkWaitTime,)
        )
        self.checkThread.start()

        if self.verbose:
            print("check procedure lancer")

    def resetCheckWaitTime(self, checkWaitTime):
        self.checkWaitTime = checkWaitTime
        self.monitor()

        if self.verbose:
            print("resetter le checkwaittime a", checkWaitTime)

    def checkDigital(self, checkWaitTime):  # => press, release & hold
        while not self.endLoopFlag:

            self.doCheckOnce()

            if self.timeCriticalMode:
                elapsedTime = time.time() - self.timeCriticalStartTime
                sleepTime = max(0, checkWaitTime - (elapsedTime % checkWaitTime))
                time.sleep(sleepTime)
            else:
                time.sleep(checkWaitTime)

            while self.pauseChecks:
                time.sleep(0.1)

        self.endLoopFlag = False  # reset a la fin pour pouvoir relancer le thread

    def doCheckOnce(self):
        # DigitalInputDevice: True si HIGH (bouton pressé si pull_up)
        if self.device.value:
            if not self.isPressed:
                self.isPressed = True
                if self.verbose:
                    print("Button pressed")
                self.funcOnPress()
            else:  # button pressed rn
                if self.verbose:
                    print("Button still pressed")
                self.funcOnHold()
        else:
            if self.isPressed:
                self.isPressed = False
                if self.verbose:
                    print("Button released")
                self.funcOnRelease()

        self.funcOnCheck()
