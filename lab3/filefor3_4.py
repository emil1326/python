import grovepi  # type: ignore
import basicPortControlSystem
import scrutteurDigital
import scrutteurAnalog

# declare hardware

potentiometre = scrutteurAnalog(1)
myDel = basicPortControlSystem(5, True)  # ==> need pwm port

# declare hardware functions


def setDelIntensity(value):
    myDel.changeState(value / 1023)  # ==> value between 0 and 1


# link hardware functions

potentiometre.setFuncOnChange(setDelIntensity)
