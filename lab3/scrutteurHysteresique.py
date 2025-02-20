import threading
import time
import grovepi  # type: ignore
from scrutteurAnalog import scrutteurAnalog


class scrutteurHysteresique:

    verbose = False

    # scrutteur = None ==> le scrutteure actif sur cet objet

    def __init__(self, port, timeCriticalMode=True, timeCriticalStartTime=0):
        # start un scrutteur analogue avc mode crtical time on de base
        self.scrutteur = scrutteurAnalog(port, timeCriticalMode, timeCriticalStartTime)

        if self.verbose:
            self.scrutteur.verbose = True
            print("fait un objet scrutteur hysterique")
