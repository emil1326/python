import threading
import time
import grovepi  # type: ignore
from grove_rgb_lcd import *


class lcdController:
    allowedPorts = [0, 1, 2]

    text = ""

    # Define color constants
    COLOR_RED = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_BLUE = (0, 0, 255)
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_YELLOW = (255, 255, 0)
    COLOR_CYAN = (0, 255, 255)
    COLOR_MAGENTA = (255, 0, 255)

    def __init__(self, port=0):
        if self.allowedPorts.__contains__(port):
            self.port = port
        else:
            raise ValueError("Port not allowed")

    def moveTextLeft(self, position):
        pass

    def setText(self, text, clearOld=True, position=0):
        if position != 0:
            text = text.rjust(len(text) + position)

        self.text = text

        if clearOld:
            setText(text)
        else:
            setText_norefresh(text)

    def setColor(self, r, g, b):
        setRGB(r, g, b)

    def setColorByName(self, color_name):
        color_map = {
            "red": self.COLOR_RED,
            "green": self.COLOR_GREEN,
            "blue": self.COLOR_BLUE,
            "white": self.COLOR_WHITE,
            "black": self.COLOR_BLACK,
            "yellow": self.COLOR_YELLOW,
            "cyan": self.COLOR_CYAN,
            "magenta": self.COLOR_MAGENTA,
        }
        if color_name in color_map:
            self.setColor(*color_map[color_name])
        else:
            raise ValueError("Color not recognized")
