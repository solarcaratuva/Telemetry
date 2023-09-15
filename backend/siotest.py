from datetime import datetime

import socketio
import sys
from aiohttp import web

sio = socketio.AsyncServer(cors_allowed_origins='*')
app = web.Application()
sio.attach(app)

arg = int(sys.argv[1])  # Argument from command line

@sio.on('connect')
async def connect(sid, environ):
    print("Client connected")
    timestamp = datetime.now().isoformat()
    await sio.emit("pack_voltage", {"timestamp": timestamp, "number": arg})
    # await sio.emit('pack_voltage', arg, room=sid)
    await sio.disconnect(sid)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=5050)
