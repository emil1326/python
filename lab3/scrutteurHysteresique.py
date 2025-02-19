import threading
import time
import grovepi  # type: ignore
from scrutteurAnalog import scrutteurAnalog


class scrutteurHysteresique:

    scrutteur = None

    verbose = False

    def __init__(self, port, timeCriticalMode=True, timeCriticalStartTime=0):
        # start un scrutteur analogue avc mode crtical time on de base
        self.scrutteur = scrutteurAnalog(port, timeCriticalMode, timeCriticalStartTime)

        if self.verbose:
            print("fait un objet scrutteur hysterique")
