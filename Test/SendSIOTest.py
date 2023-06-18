import os
import unittest

import cantools
import eventlet
import socketio

from backend.send_from_can import CANSender

bpsDB = cantools.database.load_file('../backend/CAN-messages/BPS.dbc')
motorDb = cantools.database.load_file("../backend/CAN-messages/MotorController.dbc")
powerAuxDb = cantools.database.load_file("../backend/CAN-messages/Rivanna2.dbc")


def append_zeros(original_bytes, target_length):
    # Calculate the number of zeros needed
    num_zeros = target_length - len(original_bytes)

    # If num_zeros is less than 0, then the original_bytes is already longer than target_length
    if num_zeros < 0:
        print("The original bytes is longer than the target length.")
        return original_bytes

    # Create a new bytes object with the required number of zeros
    zeros = bytearray(num_zeros)

    # Concatenate zeros and original_bytes
    result = original_bytes + zeros

    return result


def get_serial_message(db, data, message_frame_id, frame_name):
    encoded_message = db.encode_message(frame_name, data)
    encoded_message = append_zeros(encoded_message, 17)
    data_to_pi = bytearray(25)  # Create a mutable bytearray with 25 elements initialized to zero

    data_to_pi[0] = 249
    data_to_pi[1] = message_frame_id // 0x0100  # Integer division in Python is done using //
    data_to_pi[2] = message_frame_id % 0x0100
    for i in range(17):  # Python uses "range" for for-loops
        data_to_pi[i + 3] = encoded_message[i]
    data_to_pi[24] = 250

    return data_to_pi


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.sio = socketio.Server(cors_allowed_origins=["http://localhost:3000"])
        curr_path = os.path.dirname(os.path.abspath(__file__))
        can_dir = os.path.join(curr_path, "..", "backend", "CAN-messages")
        cls.CANframes = {"BPSError": cantools.database.load_file(os.path.join(can_dir, "BPS.dbc")).get_message_by_name(
            "BPSError").signal_tree,
                         "MotorControllerError": cantools.database.load_file(
                             os.path.join(can_dir, "MotorController.dbc")).get_message_by_name(
                             "MotorControllerError").signal_tree,
                         "PowerAuxError": cantools.database.load_file(
                             os.path.join(can_dir, "Rivanna2.dbc")).get_message_by_name(
                             "PowerAuxError").signal_tree,
                         "SolarCurrent": ["total_current"],
                         "BPSCellTemperature": ["high_temperature"],
                         "ECUPowerAuxCommands": ['hazards', 'brake_lights', 'headlights', 'left_turn_signal',
                                                 'right_turn_signal'],
                         "ECUMotorCommands": ['throttle', "forward_en", "reverse_en"]
                         }
        cls.sender = CANSender(cls.sio, cls.CANframes)

    def send_sio(self, message):
        app = socketio.WSGIApp(self.sio)

        @self.sio.on("connect")
        def connect(sid, environ):
            print("connected")
            self.sender.send(message)

        eventlet.wsgi.server(eventlet.listen(('localhost', 5050)), app)

    def test_send_left_blinker(self):
        left_turn_on_msg = {
            "hazards": 0,
            "brake_lights": 0,
            "headlights": 0,
            "left_turn_signal": 1,
            "right_turn_signal": 0
        }

        testmsg = get_serial_message(powerAuxDb, left_turn_on_msg, 769, "ECUPowerAuxCommands")

        self.send_sio(testmsg)

    def test_send_errors(self):
        bps_error_example = {
            "internal_communications_fault": 0,
            "internal_conversion_fault": 0,
            "weak_cell_fault": 1,
            "low_cell_voltage_fault": 0,
            "open_wiring_fault": 0,
            "current_sensor_fault": 0,
            "pack_voltage_sensor_fault": 0,
            "weak_pack_fault": 0,
            "voltage_redundancy_fault": 0,
            "fan_monitor_fault": 0,
            "thermistor_fault": 0,
            "CANBUS_communications_fault": 0,
            "always_on_supply_fault": 0,
            "high_voltage_isolation_fault": 0,
            "power_supply_12v_fault": 0,
            "charge_limit_enforcement_fault": 0,
            "discharge_limit_enforcement_fault": 0,
            "charger_safety_relay_fault": 0,
            "internal_memory_fault": 0,
            "internal_thermistor_fault": 0,
            "internal_logic_fault": 0,
        }

        testmsg = get_serial_message(bpsDB, bps_error_example, 262, "BPSError")

        self.send_sio(testmsg)


if __name__ == '__main__':
    unittest.main()
