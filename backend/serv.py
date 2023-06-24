import eventlet
import socketio
from datetime import datetime

sio = socketio.Server(cors_allowed_origins=["http://localhost:3000", "http://localhost:12345"])
app = socketio.WSGIApp(sio)

@sio.on('data')
def on_message(sid, data):
    print('Got connection from', sid)
    print(f"Received message: {data}")

    timestamp = datetime.now().isoformat()
    sio.emit("pack_voltage", {"timestamp": timestamp, "number": 100})

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5050)), app)
