from time import sleep
from grove_rgb_lcd import setRGB, setText
from lcdController import lcdController


setText("text")
sleep(0.5)
setRGB(100, 100, 100)

screen = lcdController(1)

screen.setColorByName("magenta")

sleep(1)

screen.setColorByName("blue")

screen.setText("ligne 1", line=1)
screen.setText("ligne 2", line=2)

sleep(1)

screen.setColorByName("gold")

for i in range(0, 100):
    screen.setText(f"Quick {i}", position=6, line=2)
    sleep(0.1)
