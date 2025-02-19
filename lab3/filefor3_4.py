import grovepi  # type: ignore
from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog

# declare hardware

potentiometre = scrutteurAnalog(1)
potentiometre.steps = 10
myDel = basicPortControlSystem(3, True)  # ==> need pwm port

# test hardware

myDel.pulseSync(5, 0.2, 0.2)

input("test done")

# declare hardware functions


def setDelIntensity(value):
    val = value / 1023
    myDel.changeState(val)  # ==> value between 0 and 1

    print("did value", value, "=>", val)


# start monitoring

potentiometre.monitor()

# link hardware functions

potentiometre.setFuncOnChange(setDelIntensity)

# wait for end

input("finish?")

# finish

potentiometre.endLoop()
myDel.shutDown()
