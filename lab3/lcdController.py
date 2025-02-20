import threading
import time
import grovepi  # type: ignore
from grove_rgb_lcd import *


# only works with v4 screens
# 16 * 2
class lcdController:
    allowedPorts = [0, 1, 2]  # unused rn

    defaultText = "                "
    defaultText2 = "                "

    # text = defaultText  # both lines
    # text2 = defaultText

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

        self.text = list(self.defaultText)
        self.text2 = list(self.defaultText2)

    # si wrap around sa remet les char enlever de lautre bord
    # si first line on marche juste sur la premiere ligne
    # si second line on marche juste sur la deuxieme ligne
    # si connceted, on fais les 2 ensemble; pousser of de la premiere ligne envois sur la seconde comme sils etait bout a bouts
    # fill char est ce quon remplis avc
    def moveTextLeft(
        self,
        wrapAround=False,
        firstLine=True,
        secondLine=False,
        connected=False,
        fillChar=" ",
    ):

        val = self.__moveTextLeft(
            self.text,
            self.text2,
            wrapAround,
            firstLine,
            secondLine,
            connected,
            fillChar,
        )

        self.text = val[0]
        self.text2 = val[1]

    def moveTextRight(
        self,
        wrapAround=False,
        firstLine=True,
        secondLine=False,
        connected=False,
        fillChar=" ",
    ):

        t1 = self.text
        t2 = self.text2

        t1.reverse()
        t2.reverse()

        val = self.__moveTextLeft(
            t1,
            t2,
            wrapAround,
            firstLine,
            secondLine,
            connected,
            fillChar,
        )

        val[0].reverse()
        val[1].reverse()

        self.text = t1
        self.text2 = t2

    def __moveTextLeft(
        self,
        text1,
        text2,
        wrapAround=False,
        firstLine=True,
        secondLine=False,
        connected=False,
        fillChar=" ",
    ):
        if firstLine:
            if wrapAround:
                text1.append(text1.pop(0))
            else:
                text1.pop(0)
                text1.append(fillChar)

        if secondLine:
            if wrapAround:
                text2.append(text2.pop(0))
            else:
                text2.pop(0)
                text2.append(fillChar)

        if connected:
            combined_text = text1 + text2
            if wrapAround:
                combined_text.append(combined_text.pop(0))
            else:
                combined_text.pop(0)
                combined_text.append(fillChar)
            text1 = combined_text[: len(self.defaultText)]
            text2 = combined_text[len(self.defaultText2) :]  # todo changer vers value?

        return text1, text2

    def setText(self, text, clearOldText=True, position=0):
        if clearOldText:
            self.clearText()

        # check selon les defaults
        if len(text) > len(self.defaultText) + len(self.defaultText2):
            raise ValueError("text too long to be written", text)

        for i in range(len(text)):
            curI = i + position
            # si dans premiere ligne
            if curI < len(self.defaultText):
                self.text[curI] = text[i]
            else:
                self.text2[curI - len(self.defaultText)] = text[i]

        self.printOnScreen()

    def printOnScreen(self):
        # change les array back en string
        final = "".join(self.text) + "".join(self.text2)
        setText(final)

    def clearText(self):
        self.text = list(self.defaultText)
        self.text2 = list(self.defaultText2)

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
