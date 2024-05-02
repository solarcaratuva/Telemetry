from datetime import datetime

import socketio
import eventlet
# import sys
# from aiohttp import web

sio = socketio.Server(cors_allowed_origins=["*"])
app = socketio.WSGIApp(sio)

# arg = int(sys.argv[1])  # Argument from command line
@sio.event
def connect(sid, environ):
    print("Client connected")
    timestamp = datetime.now().isoformat()
    sio.emit("pack_voltage", {"timestamp": timestamp, "number": 120})

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5050)), app)
