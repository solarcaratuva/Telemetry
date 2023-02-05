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

def action() :
    val = ser.read(100).decode('utf-8')
    current_date = datetime.now()
    timestamp = current_date.isoformat()
    sio.emit("pedal_value", {"timestamp": timestamp, "number": val})
    print("MESSAGE ID "+str(random.randint(1,20))+ " RECIEVED! VALUE IS: "+str(val))


class setInterval :
    def __init__(self,interval,action) :
        self.interval=interval
        self.action=action
        self.stopEvent=threading.Event()
        thread=threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self) :
        nextTime=time.time()+self.interval
        while not self.stopEvent.wait(nextTime-time.time()) :
            nextTime+=self.interval
            self.action()
    
inter=setInterval(1,action)

sio.start_background_task(action())

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