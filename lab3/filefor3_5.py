import grovepi  # type: ignore
from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog
from lcdController import lcdController

screen = lcdController(1)

screen.setText("my text")

screen.setColor(0, 100, 200)
