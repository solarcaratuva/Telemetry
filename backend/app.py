import random
import serial
import eventlet
import socketio
from datetime import datetime
import time

sio = socketio.Server(cors_allowed_origins=["http://localhost:3000"])
app = socketio.WSGIApp(sio)
ser = serial.Serial(port="/dev/serial0")

isRunning = False
def send_data():
    while True:
        val = ser.read(100).decode('utf-8')
        current_date = datetime.now()
        timestamp = current_date.isoformat()
        sio.emit("pedal_value", {"timestamp": timestamp, "number": val})
        print("MESSAGE ID " + str(random.randint(1, 20)) + " RECIEVED! VALUE IS: " + str(val))
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