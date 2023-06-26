import os
import sys
from datetime import datetime

import serial.tools.list_ports
from digi.xbee.devices import XBeeDevice

sys.path.append(os.path.dirname(__file__))
from decode_can_dbc import decode_dbc


def get_xbee_connection():
    BAUD_RATE = 9600
    ports = serial.tools.list_ports.comports()

    for port in ports:
        # Try to open a connection to each port.
        try:
            device = XBeeDevice(port.device, BAUD_RATE)
            if device.is_open():
                device.close()
            if not device.is_open():
                device.open()
            # If we get here, we've successfully opened a connection.
            # We can now try to read a parameter from the device.
            try:
                device.get_64bit_addr()
                return device
            except:
                continue
        except:
            # Couldn't open a connection to this port. It's either in use
            # or doesn't have an XBee connected.
            pass
    return None


def get_can_data(encoded_message: bytes):
    ints = []
    for byte in encoded_message:
        ints.append(byte)
    message_id = int.from_bytes(encoded_message[1:3], "big") #first two bytes are message id
    print(f"message id: {message_id}")
    message_body = encoded_message[3:17] #next 16 bytes are message body
    name, values = decode_dbc(message_id, message_body)
    return name, values

class CANSender:
    def __init__(self, sio, can_messages):
        self.sio = sio
        self.can_messages = can_messages

    def send(self, name, values) -> bool:
        timestamp = datetime.now().isoformat()
        print(name)
        print(values)

        if name not in self.can_messages:
            return False
        if name in ("BPSError", "MotorControllerError", "PowerAuxError"):
            errors = []
            for data in self.can_messages[name]:
                if values[data]:
                    errors.append(data)

            # print("ERRORS: " + str(errors))
            self.sio.emit(name, {"timestamp": timestamp, "array": errors})
            return True
        curr_frame = self.can_messages[name]
        for data in curr_frame:
            self.sio.emit(data, {"timestamp": timestamp, "number": values[data]})
            print("DATA: " + data + " " + str(values[data]))
        return True
