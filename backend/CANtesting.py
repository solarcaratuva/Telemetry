import atexit
import pprint
import random

import cantools
import serial


def append_int_as_le_bytes(input_bytes, integer):
    # Convert the integer to bytes in little-endian format with a length of 4 bytes
    int_bytes = integer.to_bytes(4, 'little')
    # Concatenate the input bytes with the integer bytes
    result_bytes = int_bytes + input_bytes

    return result_bytes

def get_serial_message(db, data, message_frame_id, frame_name):
    encoded_message = db.encode_message(frame_name, data)
    towrite = append_int_as_le_bytes(encoded_message, message_frame_id)
    ten = 10
    towrite += ten.to_bytes(1, 'little')
    return towrite

def send_serial_message(db, data, message_frame_id, frame_name):
    towrite = get_serial_message(db, data, message_frame_id, frame_name)
    ser.write(towrite)


# Testing
randomVal = random.randint(10, 100)
ser = serial.Serial(port="/dev/serial0", invert=True)
bpsDB = cantools.database.load_file('backend/CAN-messages/BPS.dbc')
motorDb = cantools.database.load_file("backend/CAN-messages/MotorController.dbc")
powerAuxDb = cantools.database.load_file("backend/CAN-messages/Rivanna2.dbc")
message_frame_id = 513
ex_dict = {"throttle": 200, "regen": 100, "cruise_control_speed": 123, "cruise_control_en": 1, "forward_en": 1,
           "reverse_en": 0, "motor_on": 0}

# send_serial_message(powerAuxDb, ex_dict, message_frame_id, "ECUMotorCommands")

rpm_frame_dict = {
    "battery_voltage": 5.0,  # In Volts (V)
    "battery_current": 7,  # In Amperes (A)
    "battery_current_direction": 1,  # No unit
    "motor_current": 15,  # In Amperes (A)
    "fet_temp": 20,  # In Degrees Celsius (°C)
    "motor_rpm": 200,  # In Revolutions Per Minute (RPM)
    "pwm_duty": 25.0,  # In Percentage (%)
    "lead_angle": 3.5,  # In Degrees (°)
}

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

powerAuxCommandsExample = {
    "hazards": 1,
    "brake_lights": 0,
    "headlights": 1,
    "left_turn_signal": 0,
    "right_turn_signal": 1
}

# send_serial_message(motorDb, rpm_frame_dict, 805, "MotorControllerPowerStatus")
# send_serial_message(bpsDB, bps_error_example, 262, "BPSError")
testmsg = get_serial_message(powerAuxDb, powerAuxCommandsExample, 769, "ECUPowerAuxCommands")

def get_test_msg():
    return testmsg

def exit_handler():
    print("Closing serial port")
    ser.close()


atexit.register(exit_handler)
