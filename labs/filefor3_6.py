import time
from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog
from lcdController import lcdController

screen = lcdController(1)

phrase = "Pis si y mouille y mouillera, pis si y neige on pellt'ra.                 "

for i in range(0, len(phrase) - 16):

    screen.setText(phrase[i : i + 16])

    time.sleep(0.4)
