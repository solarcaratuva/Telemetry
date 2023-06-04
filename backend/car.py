import atexit
import datetime

import eventlet
import serial
import socketio
from pip._internal.utils import subprocess

from set_time import set_system_time
from send_from_can import CANSender, get_xbee_connection
from digi.xbee.devices import XBeeDevice
import ctypes.util
import time

# XBee Mac addresses
# pit - 0013A20041C4ACC3
# car - 0013A20041C4AC5F

# ports = serial.tools.list_ports.comports()
sio = socketio.Server(cors_allowed_origins=["http://localhost:3000"])
app = socketio.WSGIApp(sio)
# ser = serial.Serial(port="/dev/serial0")

# Lists of frames for each applicable CAN message

time_offset = 0

# ... more to come

# TODO - how do we get this dynamically
XBEEPORT = "COM3"
device = get_xbee_connection()


def exit_handler():
    print("Closing serial port")
    # ser.close()
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
    # while True:
    #     # encoded_message = ser.read(64)
    #     encoded_message = None
    #     if sender.send(encoded_message):
    #         device.send_data_broadcast(encoded_message)
    #     sio.sleep(1)


@sio.event
def connect(sid, environ):
    global isRunning, sio

    sio.emit("set_time_offset", time_offset)

    if not isRunning:
        isRunning = True
        sio.start_background_task(sendData)

time_received = False
if __name__ == '__main__':
    # pit starts by looping time messages
    # Car comes on, recieves time message
    # Sends acknnoledgement
    # Pit receives ack, sneds back ack
    # Car recives ack and starts transmitting data
    def time_handler(msg):
        global time_received, time_offset
        if time_received:
            return
        msgtxt: str = msg.data.decode("utf8")
        print(f"recieved: {msgtxt}")
        if msgtxt.startswith("Time:"):
            seconds = int(msgtxt[5:])
            print(f"set time to {seconds}, was {time.time()}")
            time_offset = seconds - time.time()
            with open("/home/cwise/log_car.txt", "w+") as outfile:
                outfile.write(f"system time: {time.time()}\ntime offset:{time_offset}\ntime recieved:{seconds}")
            time_received = True
            # device.del_data_received_callback(time_received)
            device.send_data_broadcast("ack")


    device.add_data_received_callback(time_handler)
    while not time_received:
        pass
    print("continueing")
    eventlet.wsgi.server(eventlet.listen(('localhost', 5050)), app)
