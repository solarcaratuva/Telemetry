import atexit
import importlib

import serial
import random
import can
import cantools


def append_int_as_le_bytes(input_bytes, integer):
    # Convert the integer to bytes in little-endian format with a length of 4 bytes
    int_bytes = integer.to_bytes(4, 'little')
    # Concatenate the input bytes with the integer bytes
    result_bytes = int_bytes + input_bytes
    print(len(result_bytes))

    return result_bytes


# Testing
randomVal = random.randint(10, 100)
ser = serial.Serial(port="/dev/serial0", invert=True)
bpsDB = cantools.database.load_file('backend/CAN-messages/Rivanna2.dbc')
message_frame_id = 513
ex_dict = {"throttle": randomVal, "regen": 100, "cruise_control_speed": 123, "cruise_control_en": 1, "forward_en": 0, "reverse_en": 0, "motor_on": 0}
# encoded_message = bpsDB.encode_message(message_frame_id, {'low_temperature': 25, 'low_thermistor_id': 1, "high_temperature": 55, "high_thermistor_id": 2})
# ser.write(encoded_message)
data = bpsDB.encode_message("ECUMotorCommands", ex_dict)
encoded_message = can.Message(arbitration_id=message_frame_id, data=data)
towrite = append_int_as_le_bytes(data, 513)
ten = 10
towrite += ten.to_bytes(1, 'little')
print(len(towrite))
ser.write(towrite)

def exit_handler():
    print("Closing serial port")
    ser.close()


atexit.register(exit_handler)