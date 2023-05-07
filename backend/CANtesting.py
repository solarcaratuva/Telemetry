import importlib

import serial
import random
import can
import cantools

# Testing
ser = serial.Serial(port="/dev/serial0", invert=True)
bpsDB = cantools.database.load_file('backend/CAN-messages/Rivanna2.dbc')
message_frame_id = 513
ex_dict = {"throttle": 100, "regen": 100, "cruise_control_speed": 0, "cruise_control_en": 0, "forward_en": 0, "reverse_en": 0, "motor_on": 0}
# encoded_message = bpsDB.encode_message(message_frame_id, {'low_temperature': 25, 'low_thermistor_id': 1, "high_temperature": 55, "high_thermistor_id": 2})
# ser.write(encoded_message)
encoded_message = bpsDB.encode_message("ECUMotorCommands", ex_dict)
ser.write(encoded_message)