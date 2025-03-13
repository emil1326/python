from time import sleep
from lcdController import lcdController

screen = lcdController(1)

screen.setColorByName("magenta")

sleep(5)

screen.setColorByName("blue")

screen.setText("ligne 1", line=1)
screen.setText("ligne 2", line=2)

sleep(1)

screen.setColorByName("gold")

for i in range(0, 100):
    screen.setText(f"Quick {i}", position=6, line=2)
    sleep(0.1)
