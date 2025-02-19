import threading
import time
import grovepi  # type: ignore
from grove_rgb_lcd import *


class lcdController:
    allowedPorts = [0, 1, 2]

    text = ""

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
