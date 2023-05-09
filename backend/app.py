import atexit
from datetime import datetime

import cantools
import eventlet
import serial
import socketio

from decode_can_dbc import decode_dbc

# from digi.xbee.devices import XBeeDevice

sio = socketio.Server(cors_allowed_origins=["http://localhost:3000"])
app = socketio.WSGIApp(sio)
ser = serial.Serial(port="/dev/serial0")

# Lists of frames for each applicable CAN message
CANframes = {"ECUPowerAuxCommands": ['hazards', 'brake_lights', 'headlights', 'left_turn_signal', 'right_turn_signal'],
             "ECUMotorCommands": ['throttle'],
             # , 'regen', 'cruse_control_speed', 'cruise_control_en', 'forward_en', 'reverse_en', 'motor_on']
             "MotorControllerPowerStatus": ["motor_rpm"],
             "BPSError": cantools.database.load_file("backend/CAN-messages/BPS.dbc").get_message_by_name(
                 "BPSError").signal_tree,
             "MotorControllerError": cantools.database.load_file(
                 "backend/CAN-messages/MotorController.dbc").get_message_by_name("MotorControllerError").signal_tree,
             "PowerAuxError": cantools.database.load_file("backend/CAN-messages/Rivanna2.dbc").get_message_by_name(
                 "PowerAuxError").signal_tree,
             }


# ... more to come

# device = XBeeDevice("/dev/ttyUSB0", 9600)

def exit_handler():
    print("Closing serial port")
    ser.close()
    # device.close()


atexit.register(exit_handler)

isRunning = False


def sendData():  # replacement for send_data
    print("LISTENING FOR DATA")
    while True:
        encoded_message = ser.read(64)
        timestamp = datetime.now().isoformat()
        message_id = int.from_bytes(encoded_message[:4], byteorder="little")
        name, values = decode_dbc(message_id, encoded_message[4:-1])
        if name not in CANframes:
            print("INVALID")
            continue
        if name in ("BPSError", "MotorControllerError", "PowerAuxError"):
            errors = []
            for data in CANframes[name]:
                if values[data]:
                    errors.append(data)

            print("ERRORS: " + str(errors))
            sio.emit(name, {"timestamp": timestamp, "array": errors})
        curr_frame = CANframes[name]
        for data in curr_frame:
            sio.emit(data, {"timestamp": timestamp, "number": values[data]})
            print("DATA: " + data + " " + str(values[data]))
        # sio.emit(message)
        # XBEE radio also send message
        sio.sleep(1)


# def broadcast_message(message):
#     device.send_data_broadcast(message)
#
#
# def read_message():
#     return device.read_data()


def send_data():  # will be deleted after 'sendData()' is done
    while True:
        encoded_message = ser.read(64)
        current_date = datetime.now()
        timestamp = current_date.isoformat()
        message_id = int.from_bytes(encoded_message[:4], byteorder="little")
        name, values = decode_dbc(message_id, encoded_message[4:-1])
        # print(f"id: {message_id}, name: {name}, values: {values}")
        if name == "ECUMotorCommands":
            sio.emit("pedal_value", {"timestamp": timestamp, "number": values["throttle"]})
        # broadcast_message(encoded_message)
        sio.sleep(1)  # Add sleep time to control the frequency of sending data


@sio.event
def connect(sid, environ):
    global isRunning
    if not isRunning:
        isRunning = True
        sio.start_background_task(sendData)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5050)), app)
