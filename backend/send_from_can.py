from datetime import datetime
import serial.tools.list_ports
from digi.xbee.devices import XBeeDevice
import cantools

from decode_can_dbc import decode_dbc
import os
curr_path = os.path.dirname(os.path.abspath(__file__))
can_dir = os.path.join(curr_path, "CAN-messages")
CANframes = {"ECUPowerAuxCommands": ['hazards', 'brake_lights', 'headlights', 'left_turn_signal', 'right_turn_signal'],
             "ECUMotorCommands": ['throttle', "forward_en", "reverse_en"],
             "MotorControllerPowerStatus": ["motor_rpm"],
             "BPSError": cantools.database.load_file(os.path.join(can_dir, "BPS.dbc")).get_message_by_name(
                 "BPSError").signal_tree,
             "MotorControllerError": cantools.database.load_file(
                 os.path.join(can_dir, "MotorController.dbc")).get_message_by_name("MotorControllerError").signal_tree,
             "PowerAuxError": cantools.database.load_file(os.path.join(can_dir, "Rivanna2.dbc")).get_message_by_name(
                 "PowerAuxError").signal_tree,
             "BPSPackInformation": ["pack_current"],
             "BPSCellTemperature": ["high_temperature"]
             }


def get_xbee_connection():
    BAUD_RATE = 9600
    ports = serial.tools.list_ports.comports()

    for port in ports:
        # Try to open a connection to each port.
        try:
            device = XBeeDevice(port.device, BAUD_RATE)
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


class CANSender:
    def __init__(self, sio):
        self.sio = sio

    def send(self, encoded_message: bytes) -> bool:
        timestamp = datetime.now().isoformat()
        message_id = int.from_bytes(encoded_message[:4], byteorder="little")
        name, values = decode_dbc(message_id, encoded_message[4:-1])
        if name not in CANframes:
            return False
        if name in ("BPSError", "MotorControllerError", "PowerAuxError"):
            errors = []
            for data in CANframes[name]:
                if values[data]:
                    errors.append(data)

            # print("ERRORS: " + str(errors))
            self.sio.emit(name, {"timestamp": timestamp, "array": errors})
            return
        curr_frame = CANframes[name]
        for data in curr_frame:
            self.sio.emit(data, {"timestamp": timestamp, "number": values[data]})
            print("DATA: " + data + " " + str(values[data]))
        return True
