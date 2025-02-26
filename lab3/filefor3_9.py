from datetime import datetime
import grovepi  # type: ignore
from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog
from lcdController import lcdController

# declare hardware

lumiere = scrutteurAnalog(0, True)
lumiere.checkWaitTime = 1
screen = lcdController(1)

# lumiere.steps = 10 # type: ignore

# test hardware

# input("test done")

# declare hardware functions

f = open("dateTimeLum", "w")


def writeToDisk(value):
    val = (float)(1023 - value) * 10 / value

    f.write(f"{datetime.now()} , {value}\n")
    
    s = "did value", value, "=>", val
    print(s)
    screen.setText(s)


# start monitoring

lumiere.monitor()

# link hardware functions

lumiere.setFuncOnCheck(writeToDisk)

# wait for end

input("finish?")

# finish

lumiere.endLoop()
f.close()


# ==> works
