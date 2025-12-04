import serial

# Open serial port (adjust COM port or /dev/ttyUSBx as needed)
ser = serial.Serial(port="COM3", baudrate=115200, timeout=1)

# TLV request for dwm_pos_get
# Type = 0x02, Length = 0x00 (no value field)
request = bytes([0x02, 0x00])

# Send request
ser.write(request)

# Read response
response = ser.read(20)  # adjust length depending on expected payload
print("Raw response:", response)
