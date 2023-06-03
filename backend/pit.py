import atexit

import eventlet
import serial.tools.list_ports
import socketio
from digi.xbee.devices import XBeeDevice

from backend.send_from_can import CANSender

# XBee Mac addresses
# 0013A20041C4ACC3
# 0013A20041C4AC5F

ports = serial.tools.list_ports.comports()
sio = socketio.Server(cors_allowed_origins=["http://localhost:3000"])
app = socketio.WSGIApp(sio)


# ... more to come
# TODO - how do we get this dynamically
XBEEPORT = "COM3"
device = XBeeDevice(XBEEPORT, 9600)
device.open()

def exit_handler():
    print("Closing serial port")
    if device is not None and device.is_open():
        device.close()


atexit.register(exit_handler)

sender = CANSender(sio)

isRunning = False
# remove rpm
# discharge -> current
# make motor faults longer/ all faults
# white mode

def sendData():  # replacement for send_data
    print("LISTENING FOR DATA")

    def data_receive_callback(xbee_message):
        address = xbee_message.remote_device.get_64bit_addr()
        data = xbee_message.data.decode("utf8")
        sender.send(data)
        print("Received data from %s: %s" % (address, data))

    device.add_data_received_callback(data_receive_callback)

@sio.event
def connect(sid, environ):
    global isRunning
    if not isRunning:
        isRunning = True
        sio.start_background_task(sendData)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5050)), app)
