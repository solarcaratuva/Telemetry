import serial
import random

# Testing
ser = serial.Serial(port="/dev/serial0", invert=True)
print(ser.name)
val = random.randint(1,100)
ser.write(str(val).encode('utf-8'))
print("MESSAGE SENT")