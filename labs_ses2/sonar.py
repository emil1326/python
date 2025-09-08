from gpiozero import DigitalOutputDevice, DigitalInputDevice;
from time import perf_counter

class Sonar:   

    def _init(self, pinEcho, pinTrigger):
        self.echo = DigitalInputDevice(pinEcho)
        self.trigger = DigitalOutputDevice(pinTrigger, true, false)
        self.pc_start = 0
        self.distance = 0
        
    
    def when_activated():
        print('when_activated')
        self.pc_start = perf_counter()

    def when_deactivated(self):
        pc_stop = perf_counter()
        t = pc_stop - self.pc_start
        v = 0.343
        self.distance = t * v / 2
   
