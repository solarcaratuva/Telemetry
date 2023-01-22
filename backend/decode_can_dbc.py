import can
import cantools

def decode_dbc(message_id, message_data): #message_id -> frame_id, message_data -> binary representation of the message data
    with open('BPS.dbc') as bps:
        bpsDB = cantools.database.load_string(bps.read())
    with open('MotorController.dbc') as motorController:
        motorControllerDB = cantools.database.load_string(motorController.read())
    with open('MPPT.dbc') as mppt:
        mpptDB = cantools.database.load_string(mppt.read())
    with open('Rivanna2.dbc') as rivanna2:
        rivanna2DB = cantools.database.load_string(rivanna2.read())

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
