import serial
import eventlet
import socketio
from datetime import datetime
import time



sio = socketio.Server(cors_allowed_origins=["http://localhost:3000"])
app = socketio.WSGIApp(sio)
ser = serial.Serial(port="/dev/serial0")
print("Listening on: "+ser.name)

@sio.on('message')
def handle(msg):
    message = ser.read(100)
    message = message.decode('utf-8')
    sio.send(message)
    print("MESSAGE SENT: "+message)
    time.sleep(1)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5050)), app)
