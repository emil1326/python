import serial as ser
import time

# Open serial port (adjust COM port or /dev/ttyUSBx as needed)
serial = ser.Serial()
serial.port = "/dev/ttyACM0"
serial.baudrate = 115200
serial.bytesize = ser.EIGHTBITS
serial.parity = ser.PARITY_NONE
serial.stopbits = ser.STOPBITS_ONE
serial.timeout = 1

# TLV request for dwm_pos_get
# Type = 0x02, Length = 0x00 (no value field)
request = bytes([0x02, 0x00])

serial.write(b"\r\r")

time.sleep(1)

serial.write(b"lep\r")

time.sleep(1)
# Send request
serial.write(request)

time.sleep(1)

# Read response
response = serial.read(1000)  # adjust length depending on expected payload
print("Raw response:", response)
