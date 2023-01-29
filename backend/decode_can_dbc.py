import can
import cantools
from pathlib import Path

def decode_dbc(message_id, message_data): #message_id -> frame_id, message_data -> binary representation of the message data
    bpsDB = cantools.database.load_file('backend/CAN-messages/BPS.dbc')
    motorControllerDB = cantools.database.load_file('backend/CAN-messages/MotorController.dbc')
    mpptDB = cantools.database.load_file('backend/CAN-messages/MPPT.dbc')
    rivanna2DB = cantools.database.load_file('backend/CAN-messages/Rivanna2.dbc')

    #Testing
    """ 
    data = bpsDB.messages

    message_frame_id = 1062
    encoded_message = bpsDB.encode_message(message_frame_id, {'low_temperature': 25, 'low_thermistor_id': 1, "high_temperature": 55, "high_thermistor_id": 2})

    message_id = message_frame_id
    message_data = encoded_message
    """

    if message_id in bpsDB._frame_id_to_message: # First Returned Value is the Name of the Message, Second Returned Value is a Dictionary with the names and associated values
        return bpsDB._frame_id_to_message[message_id].name, bpsDB.decode_message(message_id, message_data)
    elif message_id in motorControllerDB._frame_id_to_message:
        return motorControllerDB._frame_id_to_message[message_id].name, motorControllerDB.decode_message(message_id, message_data)
    elif message_id in mpptDB._frame_id_to_message:
        return mpptDB._frame_id_to_message[message_id].name, mpptDB.decode_message(message_id, message_data)
    elif message_id in rivanna2DB._frame_id_to_message:
        return rivanna2DB._frame_id_to_message[message_id].name, rivanna2DB.decode_message(message_id, message_data)
    else:
        return "ID does not exist"

#Testing
"""
if __name__ == "__main__":
    print(decode_dbc(0, 0))
"""