import time
import grovepi  # type: ignore
from basicPortControlSystem import basicPortControlSystem
from scrutteurDigital import scrutteurDigital
from scrutteurAnalog import scrutteurAnalog
from lcdController import lcdController

screen = lcdController(1)

char0 = {0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000}

char1 = {0b00000, 0b10001, 0b00000, 0b10001, 0b00000, 0b10001, 0b00000, 0b10001}

char2 = {0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001}

char3 = {0b11011, 0b10001, 0b11011, 0b10001, 0b11011, 0b10001, 0b11011, 0b10001}

char4 = {0b11011, 0b11011, 0b11011, 0b11011, 0b11011, 0b11011, 0b11011, 0b11011}

char5 = {0b11011, 0b11111, 0b11011, 0b11111, 0b11011, 0b11111, 0b11011, 0b11111}

char6 = {0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111}

animatedChar = [
    {0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000, 0b00000},
    {0b00000, 0b10001, 0b00000, 0b10001, 0b00000, 0b10001, 0b00000, 0b10001},
    {0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001, 0b10001},
    {0b11011, 0b10001, 0b11011, 0b10001, 0b11011, 0b10001, 0b11011, 0b10001},
    {0b11011, 0b11011, 0b11011, 0b11011, 0b11011, 0b11011, 0b11011, 0b11011},
    {0b11011, 0b11111, 0b11011, 0b11111, 0b11011, 0b11111, 0b11011, 0b11111},
    {0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111, 0b11111},
]

animatedChar2 = [
    char0,
    char1,
    char2,
    char3,
    char4,
    char5,
    char6,
]

# load in memory

screen.addCharToMemory(animatedChar2)

for i in range(0,100):
    screen.setText("\x0{i}") # type: ignore
    time.sleep(.2)