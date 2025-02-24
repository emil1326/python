import grovepi  # type: ignore
from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog
from lcdController import lcdController

screen = lcdController(1)

screen.setText("Pis si y mouille y mouillera, pis si y neige on pellt'ra.")
