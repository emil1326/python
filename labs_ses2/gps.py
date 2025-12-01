import serial

class GPS:
    def __init__(self):
        #configurer le serial
        serial = serial.Serial()
        serial.port = '/dev/ttyACM0'
        serial.baudrate = 115200
        serial.bytesize = serial.EIGHTBITS
        serial.parity = serial.PARITY_NONE
        serial.stopbits = serial.STOPBITS_ONE
        serial.timeout = 1
        serial.open()
        
        self.__serial = serial