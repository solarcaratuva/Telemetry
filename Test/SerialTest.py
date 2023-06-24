import atexit

import serial.tools.list_ports
import serial

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))
from send_from_can import get_can_data


def get_serial_connection():
    ports = serial.tools.list_ports.comports()
    can_serial = None
    for port in ports:
        print(f"Attempting to connect to {port.device}")
        try:
            if port.device.startswith("/dev/ttyUSB"):
                can_serial = serial.Serial(port=port.device)
                print(f"Connected to {port.device}")
                break
        except Exception:
            print(f"Failed to connect to {port.device}")
            continue
    return can_serial


def main_loop(serconn):
    while True:
        encoded_message = ser.read(1)
        start_byte = int.from_bytes(encoded_message, "big")  # Checks for start byte as int for beginning of message
        if start_byte == 249:  # 249 is the start message byte
            encoded_message += ser.read(24)  # read rest of 25 byte message
            print(f"raw msg: {encoded_message}, length: {len(encoded_message)}")
            name, values = get_can_data(encoded_message)
            print(f"~~~~~~~~~\nRaw data: {encoded_message}\nMessage Name: {name}\nValues: {values}\n~~~~~~~~~~")

# Can format:
#   249_id1,id2_canmsg(17)_250

if __name__ == "__main__":
    ser = get_serial_connection()
    if ser is None:
        print("Could not find serial port")
        exit(-1)

    def exit_handler():
        if ser is not None and ser.is_open:
            ser.close()
        exit(0)

    atexit.register(exit_handler)

    main_loop(ser)
