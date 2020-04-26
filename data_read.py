
from datetime import datetime
import msgpack
from openpyxl import load_workbook
import serial
import time


serial_port = 'ttyS11'

ser = serial.Serial(serial_port, 115200, timeout=1)

while True:
	s = ser.read(104)
	print(s)
	#print(msgpack.unpackb(s,raw=False))
