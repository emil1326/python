import math
from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog
from lcdController import lcdController
from scrutteurDigitalDHT import scrutteurDigitalDHT

# declare hardware

humSensor = scrutteurDigitalDHT(2)
humSensor.checkWaitTime = 1  # peu pas faire moin ????

# test hardware

# input("test done")

# declare hardware functions


def checkHum(value):
    val = value

    if value:
        print("did value", value, "=>", val)
    else:
        print("Fail")


# start monitoring

humSensor.monitor()

# link hardware functions

humSensor.setFuncOnCheck(checkHum)

# wait for end

input("finish?")

# finish

humSensor.endLoop()


# Accuracy  	Humidity			±5%	RH
#               Temperature		    ±2	°C
# Sensitivity	Humidity			1%	RH
#               Temperature		    1	°C
# Repeatability	Humidity			±1%	RH
#               Temperature		    ±1	°C

# ==> works
