import threading
import time
from gpiozero import PWMOutputDevice  # type: ignore
from gpiozero import DigitalOutputDevice  # type: ignore
from gpiozero import DigitalInputDevice  # type: ignore

# j'importe directement dans le fichier les classes, puisuil est demander de n'avoir que un fichier meme si ce nest pas une bonne pratique


class Moteur:
    # in1, in2, enA, in3, in4, enB
    allowedPort = [6, 5, 13, 15, 14, 18]

    # portAvancer = portReculer = portPuissance = None

    # pForward = 0  # internal puissance back && forth
    # pBackWard = 0

    def __init__(self, portAvancer, portReculer, portPuissance):
        if portAvancer in self.allowedPort:
            self.portAvancer = DigitalOutputDevice(portAvancer)
        if portReculer in self.allowedPort:
            self.portReculer = DigitalOutputDevice(portReculer)
        if portPuissance in self.allowedPort:
            self.portPuissance = PWMOutputDevice(portPuissance)

        self.pForward = 0
        self.pBackWard = 0

        self.lastTime = time.perf_counter()
        self.rStateThread = None

    def avancer(self, puissance, duration=None):
        self.setOnForTime(puissance, False, duration)

    def reculer(self, puissance, duration=None):
        self.setOnForTime(puissance, True, duration)

    def freiner(self):
        self.setOnForTime(1, True, None)
        self.setOnForTime(1, False, None)

    def arreter(self):
        self.setOnForTime(0, True, None)
        self.setOnForTime(0, False, None)

    def setOnForTime(self, value, back, duration=None):
        if duration is None:
            duration = 1000000  # inifinite duration :p

        def reset_state():
            while time.perf_counter() - self.lastTime < duration:
                time.sleep(0.1)  # Check periodically

            if back:
                self.pBackWard = 0
            else:
                self.pForward = 0
            self.setEngine()

        if back:
            self.pBackWard = value
        else:
            self.pForward = value
        self.lastTime = time.perf_counter()  # update last time
        self.setEngine()

        if not hasattr(self, "rStateThread") or not self.rStateThread.is_alive():  # type: ignore
            self.rStateThread = threading.Thread(target=reset_state)
            self.rStateThread.start()

    def setEngine(self):
        if self.pForward > self.pBackWard:
            self.portAvancer.on()
            self.portReculer.off()
            self.portPuissance.value = self.pForward
        if self.pForward < self.pBackWard:
            self.portAvancer.off()
            self.portReculer.on()
            self.portPuissance.value = self.portReculer

    def Test(self):
        print("Test du moteur...")
        self.avancer(0.5, 2)
        time.sleep(2.5)
        self.reculer(0.5, 2)
        time.sleep(2.5)
        self.arreter()

    def shutDown(self):
        self.arreter()

        print("shutdown")


class Robot:
    # in1, in2, enA, in3, in4, enB
    allowedEnginePort = [6, 5, 13, 15, 14, 18]

    # portAvancer = portReculer = portPuissance = None

    # pForward = 0  # internal puissance back && forth
    # pBackWard = 0

    def __init__(self):
        self.Lengine = Moteur(6, 5, 13)
        self.Rengine = Moteur(15, 14, 18)

        self.pForwardL = 0
        self.pBackWardL = 0
        self.pForwardR = 0
        self.pBackWardR = 0

        self.lastTime = time.perf_counter()
        self.rStateThread = None

    def avancer(self, puissance, duration=None, awaitIT=False):
        self.setOnForTime(puissance, False, duration, "both")

        if awaitIT and duration is not None:
            time.sleep(duration)

    def reculer(self, puissance, duration=None, awaitIT=False):
        self.setOnForTime(puissance, True, duration, "both")

        if awaitIT and duration is not None:
            time.sleep(duration)

    def turnL(self, puissance, duration=None, awaitIT=False):
        self.setOnForTime(puissance, True, duration, "right")
        self.setOnForTime(0, False, duration, "left")

        if awaitIT and duration is not None:
            time.sleep(duration)

    def turnR(self, puissance, duration=None, awaitIT=False):
        self.setOnForTime(puissance, True, duration, "left")
        self.setOnForTime(0, False, duration, "right")

        if awaitIT and duration is not None:
            time.sleep(duration)

    def freiner(self):
        self.setOnForTime(1, True, None, "both")
        self.setOnForTime(1, False, None, "both")

    def arreter(self):
        self.setOnForTime(0, True, None, "both")
        self.setOnForTime(0, False, None, "both")

    def setOnForTime(self, value, back, duration=None, side="both"):
        if duration is None:
            duration = 1000000  # infinite duration :p

        def reset_state():
            while time.perf_counter() - self.lastTime < duration:
                time.sleep(0.1)  # Check periodically

            if side in ["both", "left"]:
                if back:
                    self.pBackWardL = 0
                else:
                    self.pForwardL = 0
            if side in ["both", "right"]:
                if back:
                    self.pBackWardR = 0
                else:
                    self.pForwardR = 0
            self.setEngines()

        if side in ["both", "left"]:
            if back:
                self.pBackWardL = value
            else:
                self.pForwardL = value
        if side in ["both", "right"]:
            if back:
                self.pBackWardR = value
            else:
                self.pForwardR = value

        self.lastTime = time.perf_counter()  # update last time
        self.setEngines()

        if not hasattr(self, "rStateThread") or not self.rStateThread.is_alive():  # type: ignore
            self.rStateThread = threading.Thread(target=reset_state)
            self.rStateThread.start()

    def setEngines(self):
        # Left engine
        if self.pForwardL > 0:
            self.Lengine.avancer(self.pForwardL)
        elif self.pBackWardL > 0:
            self.Lengine.reculer(self.pBackWardL)
        else:
            self.Lengine.arreter()

        # Right engine
        if self.pForwardR > 0:
            self.Rengine.avancer(self.pForwardR)
        elif self.pBackWardR > 0:
            self.Rengine.reculer(self.pBackWardR)
        else:
            self.Rengine.arreter()

    def Test(self):
        self.Lengine.Test()
        self.Rengine.Test()
        print("Test du moteur...")

        print("Avancer...")
        self.avancer(0.5, 2)
        time.sleep(2.5)

        print("Reculer...")
        self.reculer(0.5, 2)
        time.sleep(2.5)

        print("Tourner a gauche...")
        self.turnL(0.5, 2)
        time.sleep(2.5)

        print("Tourner a droite...")
        self.turnR(0.5, 2)
        time.sleep(2.5)

        print("Freiner...")
        self.freiner()
        time.sleep(2.5)

        print("Arreter...")
        self.arreter()

    def shutdown(self):
        self.arreter()
        self.Lengine.shutDown()
        self.Rengine.shutDown()


class scrutteurDigital:
    allowedPorts = [2, 3, 4, 5, 6, 7, 8]

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
            self.port = DigitalInputDevice(port)
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
        if (
            self.port.value == 1
        ):  # jamais encore essayer de read les value mais y me semble c comme sa?
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


class basicPortControlSystem:
    allowedPorts = [2, 3, 4, 5, 6, 7, 8]
    pwmPorts = [3, 5, 6, 9]
    # usePWM = False
    verbose = False

    # curState = 0  # 0 = off, 1 = on, if on pwm do * 255, only in __Update

    # timeOut = null => null -> no timeout rn, - in do not light + in light
    # lastTime = 0 => time begin timeout
    # rStateThread = none

    def __init__(self, port, usePWM=False):
        self.curState = 0
        self.timeOut = None
        self.lastTime = time.perf_counter()
        self.rStateThread = None

        if usePWM == True:
            raise ValueError("Cannot use pwm dans cet exemple")

        self.usePWM = usePWM
        if usePWM:
            if port in self.pwmPorts:
                self.port = port
            else:
                raise ValueError("Port not allowed")
        else:
            if port in self.allowedPorts:
                self.port = DigitalOutputDevice(port)
            else:
                raise ValueError("Port not allowed")

        self.__update()

    def __update(self):
        self.port.value = round(self.curState)

    def shutDown(self):
        self.changeState(0)

    def setOnForTime(self, duration, value):

        def reset_state():
            while time.perf_counter() - self.lastTime < duration:
                time.sleep(0.1)  # Check periodically

            self.curState = 0
            self.__update()

        self.curState = value
        self.lastTime = time.perf_counter()  # Update the lastTime to the current time
        self.__update()

        if self.rStateThread is None or not self.rStateThread.is_alive():
            self.rStateThread = threading.Thread(target=reset_state)
            self.rStateThread.start()

    def pulseAsync(self, times, intime, outtime=None, intensity=None):
        if outtime is None:
            outtime = intime
        if intensity is not None:
            self.curState = intensity

        t1 = threading.Thread(
            target=self.pulseSync,
            args=(
                times,
                intime,
                outtime,
            ),
        )
        t1.start()

    # si lancer directement, va bloquer juste qua la fin des pulses
    def pulseSync(self, times, intime, outtime=None):
        if outtime is None:
            outtime = intime

        for i in range(times):
            if self.verbose:
                print("Pulse ", i + 1, " of ", times)

            self.curState = 1 - self.curState
            self.__update()
            time.sleep(intime)

            self.curState = 1 - self.curState
            self.__update()

            time.sleep(outtime)

    def changeState(self, state):
        if not state >= 0 and not state <= 1:
            raise ValueError("State not allowed")

        self.curState = state
        self.__update()

        if self.verbose:
            print("Changed state to ", self.curState)

    def switchState(self):
        self.curState = 1 - self.curState
        self.__update()

        if self.verbose:
            print("Switched state to ", self.curState)


capteureIRGauche = scrutteurDigital(23)
capteureIRDroite = scrutteurDigital(24)
delVerte = basicPortControlSystem(9)
delJaune = basicPortControlSystem(10)

robot = Robot()

hasLeft = False
hasRight = False


def capteureGEnabled():
    global hasLeft
    hasLeft = True


def capteureGDisabled():
    global hasLeft
    hasLeft = False


def capteureDEnabled():
    global hasRight
    hasRight = True


def capteureDDisabled():
    global hasRight
    hasRight = False


# on fais juste set les moteures, per tick checks
def capteureOnCheck():
    setMoteures()


def setMoteures():
    # if none
    if hasLeft == False and hasRight == False:
        robot.arreter()
        delVerte.changeState(0)
        delJaune.changeState(0)
        # if left only
    elif hasLeft == True and hasRight == False:
        robot.arreter()
        robot.setOnForTime(0.5, False, side="Left")
        delVerte.changeState(1)
        delJaune.changeState(0)
        # right only
    elif hasLeft == False and hasRight == True:
        robot.arreter()
        robot.setOnForTime(0.5, False, side="Right")
        delVerte.changeState(1)
        delJaune.changeState(0)
        # tsu un mur
    elif hasLeft == True and hasRight == True:
        robot.reculer(0.5)
        delVerte.changeState(0)
        delJaune.changeState(1)
    pass


# inverted les press/disabled&enabled pcq les ir sont inverser

# on press -> quand sa change de 0 vers 1 -> quand la ligne se retire
capteureIRGauche.setFuncOnPress(capteureGDisabled)
capteureIRGauche.setFuncOnRelease(capteureGEnabled)
capteureIRDroite.setFuncOnPress(capteureDDisabled)
capteureIRDroite.setFuncOnRelease(capteureDEnabled)

capteureIRDroite.setFuncOnCheck(capteureOnCheck)

capteureIRDroite.monitor()
capteureIRGauche.monitor()

input("finish?")

# finish

capteureIRDroite.endLoop()
capteureIRGauche.endLoop()

delVerte.shutDown()
delJaune.shutDown()

robot.shutdown()


# marche surement :>
# faut juste sassurer que les ports que jai mis sont les bons pour le tester mais c senser etre les bons
# il y a pas grand choses que je peu retirer des classes, donc jai pas trop retirer edes choses, juste rajouter des check pour etre sur que y aile pas de problemes
