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

    # allText  ==> on le prend et puis avc la position on chiosi quoi show

    # charMemorySlots ==> whats inside all the slots 0-6 ==> 7 kept for dynamic

    # Define color constants
    # region Color Constants
    COLOR_RED = (255, 0, 0)
    COLOR_GREEN = (0, 255, 0)
    COLOR_BLUE = (0, 0, 255)
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    COLOR_YELLOW = (255, 255, 0)
    COLOR_CYAN = (0, 255, 255)
    COLOR_MAGENTA = (255, 0, 255)
    COLOR_ORANGE = (255, 165, 0)
    COLOR_PURPLE = (128, 0, 128)
    COLOR_PINK = (255, 192, 203)
    COLOR_BROWN = (165, 42, 42)
    COLOR_GRAY = (128, 128, 128)
    COLOR_LIGHT_BLUE = (173, 216, 230)
    COLOR_LIGHT_GREEN = (144, 238, 144)
    COLOR_LIGHT_CYAN = (224, 255, 255)
    COLOR_LIGHT_MAGENTA = (255, 182, 193)
    COLOR_LIGHT_YELLOW = (255, 255, 224)
    COLOR_DARK_RED = (139, 0, 0)
    COLOR_DARK_GREEN = (0, 100, 0)
    COLOR_DARK_BLUE = (0, 0, 139)
    COLOR_DARK_CYAN = (0, 139, 139)
    COLOR_DARK_MAGENTA = (139, 0, 139)
    COLOR_DARK_YELLOW = (139, 139, 0)
    COLOR_GOLD = (255, 215, 0)
    COLOR_SILVER = (192, 192, 192)
    COLOR_BEIGE = (245, 245, 220)
    COLOR_IVORY = (255, 255, 240)
    COLOR_NAVY = (0, 0, 128)
    COLOR_TEAL = (0, 128, 128)
    COLOR_MAROON = (128, 0, 0)
    COLOR_OLIVE = (128, 128, 0)
    COLOR_LIME = (0, 255, 0)
    COLOR_AQUA = (0, 255, 255)
    COLOR_FUCHSIA = (255, 0, 255)
    COLOR_CORAL = (255, 127, 80)
    COLOR_TURQUOISE = (64, 224, 208)
    COLOR_SKY_BLUE = (135, 206, 235)
    COLOR_VIOLET = (238, 130, 238)
    COLOR_INDIGO = (75, 0, 130)
    COLOR_CHOCOLATE = (210, 105, 30)
    COLOR_TOMATO = (255, 99, 71)
    COLOR_SALMON = (250, 128, 114)
    COLOR_KHAKI = (240, 230, 140)
    COLOR_PLUM = (221, 160, 221)
    COLOR_LAVENDER = (230, 230, 250)
    COLOR_MINT = (189, 252, 201)
    COLOR_PEACH = (255, 218, 185)
    COLOR_APRICOT = (251, 206, 177)
    # endregion

    def __init__(self, port=0):
        if self.allowedPorts.__contains__(port):
            self.port = port
        else:
            raise ValueError("Port not allowed")

        self.text = list(self.defaultText)
        self.text2 = list(self.defaultText2)
        self.allText = self.text + self.text2
        self.charMemorySlots = [False] * 7

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

    def setText(self, text, clearOldText=True, position=0, line=1):
        if clearOldText:
            self.clearText()

        # text fits within the buffer
        if len(text) + position > len(self.allText):
            raise ValueError("Text too long to be written", text)

        for i in range(len(text)):
            curI = i + position
            if line == 1:
                if curI < len(self.defaultText):
                    self.text[curI] = text[i]
                else:
                    self.text2[curI - len(self.defaultText)] = text[i]
            elif line == 2:
                if curI < len(self.defaultText):
                    self.text2[curI] = text[i]
                else:
                    self.text[curI - len(self.defaultText)] = text[i]

        # Update allText
        self.allText = self.text + self.text2
        self.printOnScreen()

    def printOnScreen(self):
        final = "".join(self.text[:16]) + "".join(self.text2[:16])
        setText(final)

    def clearText(self):
        self.text = list(self.defaultText)
        self.text2 = list(self.defaultText2)
        self.allText = self.text + self.text2

    def addCharToMemory(self, chars, startpos=0):
        for i in range(len(chars)):
            if startpos + i < 7:  # Ensure we don't exceed the available slots
                create_char(startpos + i, list(chars[i]))
                self.charMemorySlots[startpos + i] = True

    def writeSpecialChar(self, position, char):
        create_char(7, char)

        self.allText[position] = "\x07"

        self.printOnScreen()

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
            "orange": self.COLOR_ORANGE,
            "purple": self.COLOR_PURPLE,
            "pink": self.COLOR_PINK,
            "brown": self.COLOR_BROWN,
            "gray": self.COLOR_GRAY,
            "light_blue": self.COLOR_LIGHT_BLUE,
            "light_green": self.COLOR_LIGHT_GREEN,
            "light_cyan": self.COLOR_LIGHT_CYAN,
            "light_magenta": self.COLOR_LIGHT_MAGENTA,
            "light_yellow": self.COLOR_LIGHT_YELLOW,
            "dark_red": self.COLOR_DARK_RED,
            "dark_green": self.COLOR_DARK_GREEN,
            "dark_blue": self.COLOR_DARK_BLUE,
            "dark_cyan": self.COLOR_DARK_CYAN,
            "dark_magenta": self.COLOR_DARK_MAGENTA,
            "dark_yellow": self.COLOR_DARK_YELLOW,
            "gold": self.COLOR_GOLD,
            "silver": self.COLOR_SILVER,
            "beige": self.COLOR_BEIGE,
            "ivory": self.COLOR_IVORY,
            "navy": self.COLOR_NAVY,
            "teal": self.COLOR_TEAL,
            "maroon": self.COLOR_MAROON,
            "olive": self.COLOR_OLIVE,
            "lime": self.COLOR_LIME,
            "aqua": self.COLOR_AQUA,
            "fuchsia": self.COLOR_FUCHSIA,
            "coral": self.COLOR_CORAL,
            "turquoise": self.COLOR_TURQUOISE,
            "sky_blue": self.COLOR_SKY_BLUE,
            "violet": self.COLOR_VIOLET,
            "indigo": self.COLOR_INDIGO,
            "chocolate": self.COLOR_CHOCOLATE,
            "tomato": self.COLOR_TOMATO,
            "salmon": self.COLOR_SALMON,
            "khaki": self.COLOR_KHAKI,
            "plum": self.COLOR_PLUM,
            "lavender": self.COLOR_LAVENDER,
            "mint": self.COLOR_MINT,
            "peach": self.COLOR_PEACH,
            "apricot": self.COLOR_APRICOT,
        }

        if color_name in color_map:
            self.setColor(*color_map[color_name])
        else:
            raise ValueError("Color not recognized")
