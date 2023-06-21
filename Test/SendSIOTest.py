import os
import unittest

import cantools
import eventlet
import socketio

try:
    from backend.send_from_can import CANSender
except ModuleNotFoundError:
    from send_from_can import CANSender

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
        cls.sio = socketio.Server(cors_allowed_origins=["http://localhost:3000", "http://localhost:12345"])
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
                         "ECUMotorCommands": ['throttle', "forward_en", "reverse_en"],
                         "MotorControllerPowerStatus": ["motor_rpm"],
                         "SolarVoltage": ["panel1_voltage", "panel2_voltage", "panel3_voltage", "panel4_voltage"],
                         "SolarTemp": ["panel1_temp", "panel2_temp", "panel3_temp", "panel4_temp"],
                         "BPSPackInformation": ["pack_voltage", "pack_current", "is_charging_signal_status"]
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
            "hazards": 1,
            "brake_lights": 1,
            "headlights": 0,
            "left_turn_signal": 1,
            "right_turn_signal": 0
        }

        testmsg = get_serial_message(powerAuxDb, left_turn_on_msg, 769, "ECUPowerAuxCommands")

        self.send_sio(testmsg)

    def test_bps_errors(self):
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

    def test_motor_error(self):
        motor_controller_error = {
            "analog_sensor_err": 0,
            "motor_current_sensor_u_err": 0,
            "motor_current_sensor_w_err": 0,
            "fet_thermistor_err": 0,
            "battery_voltage_sensor_err": 0,
            "battery_current_sensor_err": 0,
            "battery_current_sensor_adj_err": 0,
            "motor_current_sensor_adj_err": 0,
            "accelerator_position_err": 0,
            "controller_voltage_sensor_err": 0,
            "power_system_err": 0,
            "overcurrent_err": 0,
            "overvoltage_err": 1,
            "overcurrent_limit": 0,
            "motor_system_err": 0,
            "motor_lock": 0,
            "hall_sensor_short": 0,
            "hall_sensor_open": 0,
            "overheat_level": 0,
        }
        testmsg = get_serial_message(motorDb, motor_controller_error, 277, "MotorControllerError")

        self.send_sio(testmsg)

    def test_ecu_commands(self):
        ecu_motor_commands = {
            "throttle": 255,
            "regen": 0,
            "cruise_control_speed": 0,
            "cruise_control_en": 0,
            "forward_en": 0,
            "reverse_en": 0,
            "motor_on": 0
        }
        testmsg = get_serial_message(powerAuxDb, ecu_motor_commands, 513, "ECUMotorCommands")

        self.send_sio(testmsg)

    def test_motor_power_status(self):
        motor_controller_power_status = {
            "battery_voltage": 0,
            "battery_current": 0,
            "battery_current_direction": 0,
            "motor_current": 0,
            "fet_temp": 0,
            "motor_rpm": 100,
            "pwm_duty": 0,
            "lead_angle": 0,
        }
        testmsg = get_serial_message(motorDb, motor_controller_power_status, 805, "MotorControllerPowerStatus")

        self.send_sio(testmsg)

    def test_solar_current(self):
        solar_current_example = {
            "total_current": 30
        }
        testmsg = get_serial_message(powerAuxDb, solar_current_example, 1076, "SolarCurrent")

        self.send_sio(testmsg)

    def test_battery_temp(self):
        bps_cell_temperature_example = {
            "low_temperature": 0,
            "low_thermistor_id": 0,
            "high_temperature": 100,
            "high_thermistor_id": 0
        }
        testmsg = get_serial_message(bpsDB, bps_cell_temperature_example, 1062, "BPSCellTemperature")

        self.send_sio(testmsg)

if __name__ == '__main__':
    unittest.main()
