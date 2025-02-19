import grovepi  # type: ignore
from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog

# declare hardware

potentiometre = scrutteurAnalog(1)
myDel = basicPortControlSystem(5, True)  # ==> need pwm port

# declare hardware functions


def setDelIntensity(value):
    myDel.changeState(value / 1023)  # ==> value between 0 and 1


# start monitoring

potentiometre.monitor()

# link hardware functions

potentiometre.setFuncOnChange(setDelIntensity)

# wait for end

input("finish?")

# finish monitoring

potentiometre.endLoop()
