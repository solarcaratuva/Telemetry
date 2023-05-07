import random
import serial
import eventlet
import socketio
from datetime import datetime
import time
import struct
from decode_can_dbc import decode_dbc
import atexit


sio = socketio.Server(cors_allowed_origins=["http://localhost:3000"])
app = socketio.WSGIApp(sio)
ser = serial.Serial(port="/dev/serial0")


def exit_handler():
    print("Closing serial port")
    ser.close()


atexit.register(exit_handler)


def extract_frame_id(encoded_message):
    frame_id = (encoded_message[0] << 3) | (encoded_message[1] >> 5)

    # Check if the frame is an extended frame (29-bit ID)
    if (encoded_message[1] & 0x08) != 0:
        # Add the remaining bits to the frame_id (18 bits)
        frame_id = (frame_id << 2) | (encoded_message[1] & 0x03)
        frame_id = (frame_id << 8) | encoded_message[2]
        frame_id = (frame_id << 8) | encoded_message[3]
        # Skip 4 bytes (ID and DLC) when reading data bytes
        data_offset = 4
    else:
        # Skip 2 bytes (ID and DLC) when reading data bytes
        data_offset = 2

    return frame_id, data_offset


isRunning = False


def send_data():
    while True:
        encoded_message = ser.read(64)
        current_date = datetime.now()
        timestamp = current_date.isoformat()
        message_id = int.from_bytes(encoded_message[:4], byteorder="little")
        name, values = decode_dbc(message_id, encoded_message[4:-1])
        print(f"id: {message_id}, name: {name}, values: {values}")
        sio.emit("pedal_value", {"timestamp": timestamp, "number": 100})
        sio.sleep(1)  # Add sleep time to control the frequency of sending data


@sio.event
def connect(sid, environ):
    print('connect ', sid)
    global isRunning
    if not isRunning:
        isRunning = True
        sio.start_background_task(send_data)


@sio.event
def my_message(sid, data):
    print('message ', data)


@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5050)), app)

"""
import serial, socketio, json, time

ser = serial.Serial(port="/dev/serial0")
sio = socketio.Server()

# PySerial testing
print("Listening on: "+ser.name)
while True:
    message = ser.read(100).decode('utf-8')
    print(message)
    print("MESSAGE RECIEVED")


while True:
    data = serial.read(1000).decode('utf-8')
    message = decode_can_dbc(0, data)
    json = json.dumps(message)
    sio.emit("event", json)
   
    time.sleep(0.01)
"""
