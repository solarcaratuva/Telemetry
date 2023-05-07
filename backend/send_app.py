import random
import serial
import eventlet
import socketio
from datetime import datetime
import time
import struct
from decode_can_dbc import decode_dbc
from digi.xbee.devices import XBeeDevice


sio = socketio.Server(cors_allowed_origins=["http://localhost:3000"])
app = socketio.WSGIApp(sio)
ser = serial.Serial(port="/dev/serial0")
device = XBeeDevice("/dev/ttyUSB0", 9600)


def extract_message_id(can_message):
    message_id = int.from_bytes(can_message[:4], byteorder='big') >> 21
    return message_id

def broadcast_message(name,values):
    device.open()
    device.send_data_broadcast(name+values)
    device.close()

isRunning = False


def send_data():
    while True:
        encoded_message = ser.read(8)
        current_date = datetime.now()
        timestamp = current_date.isoformat()
        name, values = decode_dbc(extract_message_id(encoded_message), encoded_message)
        print(name)
        print(values)
        sio.emit("pedal_value", {"timestamp": timestamp, "number": 100})
        broadcast_message(name,values)
        print("MESSAGE ID " + str(random.randint(1, 20)) + " RECIEVED! VALUE IS: " + str(encoded_message))
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