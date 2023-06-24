import os

import can
import cantools
from pathlib import Path
import binascii
import codecs

def decode_dbc(message_id, message_data): #message_id -> frame_id, message_data -> binary representation of the message data
    # Switch comment below and uncomment line 2 below for testing, vice versa for prod
    message = make_hex_great_again(message_data)
    # message = message_data

    # message_id = make_hex_great_again(message_id)

    curr_path = os.path.dirname(os.path.abspath(__file__))
    can_dir = os.path.join(curr_path, "CAN-messages")

    bpsDB = cantools.database.load_file(os.path.join(can_dir, "BPS.dbc"))
    motorControllerDB = cantools.database.load_file(os.path.join(can_dir, "MotorController.dbc"))
    mpptDB = cantools.database.load_file(os.path.join(can_dir, "MPPT.dbc"))
    rivanna2DB = cantools.database.load_file(os.path.join(can_dir, "Rivanna2.dbc"))

    #Testing
    # data = bpsDB.messages
    #
    # message_frame_id = 1062
    # encoded_message = bpsDB.encode_message(message_frame_id, {'low_temperature': 25, 'low_thermistor_id': 1, "high_temperature": 55, "high_thermistor_id": 2})
    #
    # message_id = message_frame_id
    # message_data = encoded_message

    if message_id in bpsDB._frame_id_to_message: # First Returned Value is the Name of the Message, Second Returned Value is a Dictionary with the names and associated values
        return bpsDB._frame_id_to_message[message_id].name, bpsDB.decode_message(message_id, message)
    elif message_id in motorControllerDB._frame_id_to_message:
        return motorControllerDB._frame_id_to_message[message_id].name, motorControllerDB.decode_message(message_id, message)
    elif message_id in mpptDB._frame_id_to_message:
        return mpptDB._frame_id_to_message[message_id].name, mpptDB.decode_message(message_id, message)
    elif message_id in rivanna2DB._frame_id_to_message:
        return rivanna2DB._frame_id_to_message[message_id].name, rivanna2DB.decode_message(message_id, message)
    else:
        return "ID does not exist"
        
def make_hex_great_again(message_data):
    ints = []
    for x in message_data:
        ints.append(x)
    new_message = ""
    for x in ints: #manually convert int to hex
        if x>=48 and x <= 57:
            new_message += hex(x-48)[2:]
        elif x>=65 and x <= 70:
            new_message += hex(x-55)[2:]
        else:
            new_message += hex(0)[2:]
    return codecs.decode(new_message, 'hex_codec')
                
