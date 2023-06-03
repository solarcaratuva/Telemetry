from datetime import datetime

import cantools

from backend.decode_can_dbc import decode_dbc

CANframes = {"ECUPowerAuxCommands": ['hazards', 'brake_lights', 'headlights', 'left_turn_signal', 'right_turn_signal'],
             "ECUMotorCommands": ['throttle', "forward_en", "reverse_en"],
             "MotorControllerPowerStatus": ["motor_rpm"],
             "BPSError": cantools.database.load_file("backend/CAN-messages/BPS.dbc").get_message_by_name(
                 "BPSError").signal_tree,
             "MotorControllerError": cantools.database.load_file(
                 "backend/CAN-messages/MotorController.dbc").get_message_by_name("MotorControllerError").signal_tree,
             "PowerAuxError": cantools.database.load_file("backend/CAN-messages/Rivanna2.dbc").get_message_by_name(
                 "PowerAuxError").signal_tree,
             "BPSPackInformation": ["pack_current"],
             "BPSCellTemperature": ["high_temperature"]
             }

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
