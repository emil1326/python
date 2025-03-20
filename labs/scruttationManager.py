import threading
import time


class scruttationManager:
    verbose = False

    # takes in scrutteurs and thread them better when a lot of scrutteures work together
    # devrais pas avoir plusieur fois se component

    # scrutteures = [] # ==> liste de tout les scrutteurs

    # checkThread = None  # ==> thread object
    # checkWaitTime = 0.05  # ==> changer sert a rien sans faire check()
    # pauseChecks = False  # ==> pause le check
    # endLoopFlag = False  # ==> end loop
    # timeCriticalMode = False
    # time critical mode, is on on utulise le start time pour avoir le debut de la loop a un moment precis,
    # pour jamais devier, mieux que off pour regulariter mais plus de prosseceur utuliser
    # timeCriticalStartTime = 0

    # funcOnCheck = None

    def __init__(self, timeCriticalMode=False, timeCriticalStartTime=0.0):

        self.scrutteures = []

        self.checkThread = None
        self.checkWaitTime = 0.05
        self.pauseChecks = False
        self.endLoopFlag = False

        self.timeCriticalMode = timeCriticalMode
        self.timeCriticalStartTime = timeCriticalStartTime

        self.funcOnCheck = self.passFunc

        if self.verbose:
            print("Creer object digi scrutteur")

    def passFunc(self):
        pass

    def setFuncOnCheck(self, func):
        self.funcOnCheck = func

        if self.verbose:
            print("setted function", func, "on check")

    def addScrutteur(self, scrutteur):
        scrutteur.endLoop()
        self.scrutteures.append(scrutteur)

    def removeScrutteur(self, scrutteur):
        self.scrutteures.remove(scrutteur)

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
            target=self.monitorSync, args=(self.checkWaitTime,)
        )
        self.checkThread.start()

        if self.verbose:
            print("check procedure lancer")

    def resetCheckWaitTime(self, checkWaitTime):
        self.checkWaitTime = checkWaitTime
        self.monitor()

        if self.verbose:
            print("resetter le checkwaittime a", checkWaitTime)

    def monitorSync(self, checkWaitTime):  # => press, release & hold
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

        # ==> check tout les scrutteurs, si err sa veut dire tas mis une classe qui marche pas avc sa
        for s in self.scrutteures:
            s.doCheckOnce()

        self.funcOnCheck()
