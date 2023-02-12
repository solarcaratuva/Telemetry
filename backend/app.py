import random
import serial
import eventlet
import socketio
from datetime import datetime
import time, threading



sio = socketio.Server(cors_allowed_origins=["http://localhost:3000"])
app = socketio.WSGIApp(sio)
ser = serial.Serial(port="/dev/serial0")
print("Listening on: "+ser.name)

#val = ser.read(100).decode('utf-8')
#val = random.randint(1, 100)

@sio.event
def connect(sid, environ):
    print('connect ', sid)


@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

def main():
    while True:
        message = ser.read(100).decode('utf-8')
        sio.emit(message)
        print("MESSAGE SENT: "+message)

t1 = threading.Thread(target=main, name='t1')
t1.start()
print("THREAD STARTED")

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5050)), app)

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