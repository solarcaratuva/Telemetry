import atexit
import eventlet
import serial
import socketio
from backend.send_from_can import CANSender
from digi.xbee.devices import XBeeDevice

# XBee Mac addresses
# pit - 0013A20041C4ACC3
# car - 0013A20041C4AC5F

# ports = serial.tools.list_ports.comports()
sio = socketio.Server(cors_allowed_origins=["http://localhost:3000"])
app = socketio.WSGIApp(sio)
ser = serial.Serial(port="/dev/serial0")

# Lists of frames for each applicable CAN message



# ... more to come

# TODO - how do we get this dynamically
XBEEPORT = "COM3"
device = XBeeDevice(XBEEPORT, 9600)
device.open()

def exit_handler():
    print("Closing serial port")
    ser.close()
    if device is not None and device.is_open():
        device.close()


atexit.register(exit_handler)

sender = CANSender(sio)

isRunning = False
# remove rpm
# discharge -> current
# make motor faults longer/ all faults
# white mode

def sendData():
    print("LISTENING FOR DATA")
    while True:
        encoded_message = ser.read(64)
        if sender.send(encoded_message):
            device.send_data_broadcast(encoded_message)
        sio.sleep(1)


@sio.event
def connect(sid, environ):
    global isRunning
    if not isRunning:
        isRunning = True
        sio.start_background_task(sendData)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 5050)), app)
