import serial

ser = serial.Serial(port="/dev/serial/by-id/usb-Teensyduino_USB_Serial_6538150-if00", baudrate=9600)

while True:
    curr = ser.read(1)
    print(curr)