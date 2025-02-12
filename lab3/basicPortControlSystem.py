import time
import grovepi  # type: ignore


class basicPortControlSystem:
    allowedPorts = [2, 3, 4, 7, 8]
    pwmPorts = [3, 5, 6, 9]
    usePWM = False
    verbose = False

    curState = 0  # 0 = off, 1 = on, if on pwm do * 255, only in __Update

    def __init__(self, port, usePWM=False):
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

        grovepi.pinMode(self.port, "OUTPUT")

    def __update(self):
        if self.usePWM:
            grovepi.analogWrite(self.port, self.curState * 255)
        else:
            grovepi.digitalWrite(self.port, self.curState)

    def flash(self, times, intime, outtime=None, intensity=None):
        if outtime is None:
            outtime = intime
        if intensity is not None:
            self.curState = intensity

        for i in range(times):
            self.curState = not self.curState
            self.__update()
            time.sleep(intime)

            self.curState = not self.curState
            self.__update()
            time.sleep(outtime)

            if self.verbose:
                print("Flash ", i + 1, " of ", times)

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
