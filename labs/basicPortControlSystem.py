import threading
import time
import grovepi  # type: ignore


class basicPortControlSystem:
    allowedPorts = [2, 3, 4, 5, 6, 7, 8]
    pwmPorts = [3, 5, 6, 9]
    # usePWM = False
    verbose = False

    # curState = 0  # 0 = off, 1 = on, if on pwm do * 255, only in __Update

    def __init__(self, port, usePWM=False):
        self.curState = 0

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
