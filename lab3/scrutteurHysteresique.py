import threading
import time
import grovepi  # type: ignore
from scrutteurAnalog import scrutteurAnalog


class scrutteurHysteresique:

    verbose = False
    
    waitTimeEntreStates = 10
    offBound = 0.4
    onBound = 0.6
    
    # scrutteur = None ==> le scrutteure actif sur cet objet

    def __init__(self, port, timeCriticalMode=True, timeCriticalStartTime=0):
        # start un scrutteur analogue avc mode crtical time on de base
        self.scrutteur = scrutteurAnalog(port, timeCriticalMode, timeCriticalStartTime)
        
        self.startTime = time.perf_counter()

        if self.verbose:
            self.scrutteur.verbose = True
            print("fait un objet scrutteur hysterique")

    def getCurrState(self):
        
        
        
        return None
    
    def Monitor(self):
        self.scrutteur.monitor()
        
    