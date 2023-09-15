import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('Connected to server')
    sio.emit('data', 'Hello, Server!')

@sio.event
def pack_voltage(data):
    print('Received pack_voltage:', data)

sio.connect('http://localhost:5050')
