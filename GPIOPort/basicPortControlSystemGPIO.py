import threading
import time
import grovepi  # type: ignore


class basicPortControlSystemGPIO:
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

        self.usePWM = usePWM
        if usePWM:
            if port in self.pwmPorts:
                self.port = port
            else:
                raise ValueError("Port not allowed")
        else:
            if port in self.allowedPorts:
                self.port = port
            else:
                raise ValueError("Port not allowed")

        self.__update()

        grovepi.pinMode(self.port, "OUTPUT")

    def __update(self):
        if self.usePWM:
            grovepi.analogWrite(self.port, round(self.curState * 255))
        else:
            grovepi.digitalWrite(self.port, round(self.curState))

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
