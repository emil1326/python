import serial as ser
import time

class RadioNavigation:
    def __init__(self):
        #configurer le serial
        serial = ser.Serial()
        serial.port = '/dev/ttyACM0'
        serial.baudrate = 115200
        serial.bytesize = ser.EIGHTBITS
        serial.parity = ser.PARITY_NONE
        serial.stopbits = ser.STOPBITS_ONE
        serial.timeout = 1
        
        serial.open()
        
        
        self.__serial = serial
    
    def demarrer(self):
        try:
            self.__serial.write(b'\r\r')
            
            time.sleep(1)
            
            self.__serial.write(b'lep\r')
            return True
        except Exception as e:                        
            print("Impossible de demarrer la radio navigation", e)
            return False
    
    def get_position(self):        
        time.sleep(0.1)
        data = str(self.__serial.readline())
        print('data: ', data)
        