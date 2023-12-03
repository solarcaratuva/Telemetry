import eventlet
eventlet.patcher.monkey_patch(socket=True)
import os.path
import sys
from datetime import datetime
from queue import Queue
from threading import Thread

import serial
import socketio

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))
from backend.send_from_can import get_xbee_connection

device = get_xbee_connection()
if device is None:
    print("Couldn't connect to radio")
    exit(-1)

sio = socketio.Server(cors_allowed_origins=["http://localhost:3000", "http://localhost:12345"])
app = socketio.WSGIApp(sio)

queue = Queue()

def sendData():  # replacement for send_data
    print("LISTENING FOR DATA")

    def data_receive_callback(xbee_message):
        address = xbee_message.remote_device.get_64bit_addr()
        data = xbee_message.data.decode("utf8")
        print("Received data from %s: %s" % (address, data))
        queue.put(data)  # Put the data in queue

    device.add_data_received_callback(data_receive_callback)
    # while True:
    #     queue.put(44)

def sendSocketIoData():
    while True:
        data = queue.get(block=True)  # Wait for data in queue
        # data = 33
        print(f"{data} sdfsdf")
        timestamp = datetime.now().isoformat()
        sio.emit("pack_voltage", {"timestamp": timestamp, "number": int(data)})
        sio.sleep(1)

isRunning = False
@sio.event
def connect(sid, environ):
    global isRunning
    if not isRunning:
        isRunning = True
        Thread(target=sendData).start()
        sio.start_background_task(sendSocketIoData)

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5050)), app)
