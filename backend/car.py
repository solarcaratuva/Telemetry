import atexit
from datetime import datetime

import eventlet
import serial
import socketio
from backend.send_from_can import CANSender
from digi.xbee.devices import XBeeDevice
import ctypes.util
import time

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


def linux_set_time(seconds: int):
    # /usr/include/linux/time.h:
    #
    # define CLOCK_REALTIME                     0
    CLOCK_REALTIME = 0

    # /usr/include/time.h
    #
    # struct timespec
    #  {
    #    __time_t tv_sec;            /* Seconds.  */
    #    long int tv_nsec;           /* Nanoseconds.  */
    #  };
    class timespec(ctypes.Structure):
        _fields_ = [("tv_sec", ctypes.c_long),
                    ("tv_nsec", ctypes.c_long)]

    librt = ctypes.CDLL(ctypes.util.find_library("rt"))

    ts = timespec()
    ts.tv_sec = seconds
    ts.tv_nsec = 0  # Millisecond to nanosecond

    # http://linux.die.net/man/3/clock_settime
    librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))


time_received = False
if __name__ == '__main__':
    # pit starts by looping time messages
    # Car comes on, recieves time message
    # Sends acknnoledgement
    # Pit receives ack, sneds back ack
    # Car recives ack and starts transmitting data
    def time_handler(msg):
        global time_received
        msgtxt: str = msg.data.decode("utf8")
        if msgtxt.startswith("Time:"):
            print(f"set time to {msgtxt[5:]}")
            linux_set_time(int(int(msgtxt[5:])/1000))
            time_received = True
            device.del_data_received_callback(time_received)


    device.add_data_received_callback(time_handler)
    while not time_received:
        pass
    eventlet.wsgi.server(eventlet.listen(('localhost', 5050)), app)
