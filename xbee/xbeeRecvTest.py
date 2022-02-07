import time
import serial

ser = serial.Serial('/dev/ttyUSB1', 9600)

string = ""
while True:
    while ser.in_waiting:
        byt = ser.read(1).decode()
        string += byt
        if byt == '\n':
            print(string)
            string = ""
