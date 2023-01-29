import random

import eventlet
import socketio
from datetime import datetime

sio = socketio.Server(cors_allowed_origins=["http://localhost:3000"])
app = socketio.WSGIApp(sio)

@sio.event
def connect(sid, environ):
    print('connect ', sid)
    current_date = datetime.now()
    timestamp = current_date.isoformat()
    sio.emit("pedal_value", {"timestamp": timestamp, "number": random.randint(1, 100)})

@sio.event
def my_message(sid, data):
    print('message ', data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5050)), app)