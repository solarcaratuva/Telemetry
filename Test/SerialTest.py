import atexit

import serial.tools.list_ports
import serial

from backend.send_from_can import get_can_data


def get_serial_connection():
    ports = serial.tools.list_ports.comports()
    can_serial = None
    for port in ports:
        print(f"Attempting to connect to {port.device}")
        try:
            can_serial = serial.Serial(port=port.device)
            print(f"Connected to {port.device}")
        except Exception:
            print(f"Failed to connect to {port.device}")
            continue
    return can_serial


def main_loop(serconn):
    while True:
        txt = serconn.read(25)
        name, values = get_can_data(txt)
        print(f"~~~~~~~~~\nRaw data: {txt}\nMessage Name: {name}\nValues: {values}\n~~~~~~~~~~")

# Can format:
#   249_id1,id2_canmsg(17)_250

if __name__ == "__main__":
    ser = get_serial_connection()
    if ser is None:
        print("Could not find serial port")
        exit(-1)

    def exit_handler():
        if ser is not None and ser.is_open():
            ser.close()
        exit(0)

    atexit.register(exit_handler)

    main_loop(ser)