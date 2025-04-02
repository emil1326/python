import math
import threading
import time
import grovepi  # type: ignore


class scrutteurAnalogDHT:
    allowedPorts = [2, 3, 4, 5, 6]

    verbose = False
    allVerbose = False

    # steps = None  # ==> espacement entre les valeures analogiques possible

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
    # oldValueTemp = 0 # => old value for calculating onchange temperature
    # oldValueHum = 0 # => old value for calculating onchange humdity

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

        self.valueRange = {"minTemp": -200, "maxTemp": 200, "minHum": 0, "maxHum": 200}

        self.funcOnMinTemp = self.passFunc
        self.funcOnMaxTemp = self.passFunc
        self.funcOnChangeTemp = self.passFunc
        self.funcOnBetweenTemp = self.passFunc

        self.funcOnMinHum = self.passFunc
        self.funcOnMaxHum = self.passFunc
        self.funcOnChangeHum = self.passFunc
        self.funcOnBetweenHum = self.passFunc

        self.funcOnCheck = self.passFunc

        self.oldValueTemp = 0
        self.oldValueHum = 0

        self.steps = None

        grovepi.pinMode(self.port, "INPUT")

        if self.verbose:
            print("Creer object analog scrutteur")

    def passFunc(self, value):
        pass

    # temp
    def setFuncOnMinTemp(self, func):
        self.funcOnMinTemp = func

    def setFuncOnMaxTemp(self, func):
        self.funcOnMaxTemp = func

    def setFuncOnBetweenTemp(self, func):
        self.funcOnBetweenTemp = func

    def setFuncOnChangeTemp(self, func):
        self.funcOnChangeTemp = func

    # hum
    def setFuncOnMinHum(self, func):
        self.funcOnMinHum = func

    def setFuncOnMaxHum(self, func):
        self.funcOnMaxHum = func

    def setFuncOnBetweenHum(self, func):
        self.funcOnBetweenHum = func

    def setFuncOnChangeHum(self, func):
        self.funcOnChangeHum = func

    # on check
    def setFuncOnCheck(self, func):
        self.funcOnCheck = func

    # min max
    def setMinTemp(self, min_val):
        self.valueRange["minTemp"] = min_val

    def setMaxTemp(self, max_val):
        self.valueRange["maxTemp"] = max_val

    def setMinHum(self, min_val):
        self.valueRange["minHum"] = min_val

    def setMaxHum(self, max_val):
        self.valueRange["maxHum"] = max_val

    def setMinMax(self, min_val_temp, max_val_temp, min_val_hum, max_val_hum):
        self.setMinTemp(min_val_temp)
        self.setMaxTemp(max_val_temp)
        self.setMinHum(min_val_hum)
        self.setMaxHum(max_val_hum)

    # loop
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
            humidity = self.oldValueHum
            temp = self.oldValueTemp

        # need do temp then hum

        if self.steps != None:
            temp = self.__getStepped(self.steps, temp)
            humidity = self.__getStepped(self.steps, humidity)

        # temp ------

        if temp <= self.valueRange["minTemp"]:
            self.funcOnMinTemp(temp)
            if self.verbose:
                print("Min temp value reached:", temp)

        elif temp >= self.valueRange["maxTemp"]:
            self.funcOnMaxTemp(temp)
            if self.verbose:
                print("Max temp value reached:", temp)
            else:
                self.funcOnBetweenTemp(temp)
                if self.verbose:
                    print("Is in between temp value:", temp)

        #

        if temp != self.oldValueTemp:
            self.funcOnChangeTemp(temp)
            if self.verbose and self.allVerbose:
                print("Temp Value changed:", temp)

        # hum -------

        if humidity <= self.valueRange["minHum"]:
            self.funcOnMinHum(humidity)
            if self.verbose:
                print("Min hum value reached:", humidity)

        elif humidity >= self.valueRange["maxHum"]:
            self.funcOnMaxHum(humidity)
            if self.verbose:
                print("Max Hum value reached:", humidity)
            else:
                self.funcOnBetweenHum(humidity)
                if self.verbose:
                    print("Is in between Hum value:", humidity)

        #

        if humidity != self.oldValueHum:
            self.funcOnChangeHum(humidity)
            if self.verbose and self.allVerbose:
                print("Hum Value changed:", humidity)

        # check

        self.funcOnCheck([temp, humidity])
        if self.verbose and self.allVerbose:
            print("Value checked:", [temp, humidity])

        self.oldValueHum = humidity
        self.oldValueTemp = temp
