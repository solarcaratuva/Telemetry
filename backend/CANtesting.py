import importlib

import serial
import random
import can
import cantools

# Testing
ser = serial.Serial(port="/dev/serial0", invert=True)

bpsDB = cantools.database.load_file('backend/CAN-messages/BPS.dbc')
message_frame_id = 1062
encoded_message = bpsDB.encode_message(message_frame_id, {'low_temperature': 25, 'low_thermistor_id': 1, "high_temperature": 55, "high_thermistor_id": 2})
ser.write(encoded_message)