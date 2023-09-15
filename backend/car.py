# Runs on the PI, takes data off ECU board over UART, parses CAN and publishes to server
import atexit
import os
import threading
import time
from queue import Queue

import cantools
import eventlet
import serial
import socketio
from digi.xbee.devices import XBeeDevice

import Config
from send_from_can import CANSender, get_xbee_connection

# XBee Mac addresses
# pit - 0013A20041C4ACC3
# car - 0013A20041C4AC5F

# USB port on PI (UART splitter)
# ser = serial.Serial("/dev/ttyUSB1", 19200)
sio = socketio.Server(cors_allowed_origins=["http://localhost:3000", "http://localhost:12345"])
app = socketio.WSGIApp(sio)
# ser = serial.Serial(port="/dev/serial0")

curr_path = os.path.dirname(os.path.abspath(__file__))
can_dir = os.path.join(curr_path, "CAN-messages")
# Lists of frames for each applicable CAN message
CANframes = {"BPSError": cantools.database.load_file(os.path.join(can_dir, "BPS.dbc")).get_message_by_name(
    "BPSError").signal_tree,
             "MotorControllerError": cantools.database.load_file(
                 os.path.join(can_dir, "MotorController.dbc")).get_message_by_name("MotorControllerError").signal_tree,
             "PowerAuxError": cantools.database.load_file(os.path.join(can_dir, "Rivanna2.dbc")).get_message_by_name(
                 "PowerAuxError").signal_tree,
             "BPSCellTemperature": ["high_temperature"],
             "ECUPowerAuxCommands": ['hazards', 'brake_lights', 'headlights', 'left_turn_signal', 'right_turn_signal'],
             "ECUMotorCommands": ['throttle', "forward_en", "reverse_en"],
             "MotorControllerPowerStatus": ["motor_rpm"],
             "BPSPackInformation": ["pack_voltage", "pack_current"]
             }


if Config.USE_RADIO:
    device = XBeeDevice("/dev/radio", 9600)
    device.open()
    pass
ser = serial.Serial(port="/dev/canUART", baudrate=19200)

# logfilename = "/home/cwise/carlogger.txt"
# with open(logfilename, "w") as outfile:
#     outfile.write("")

def exit_handler():
    if ser is not None and ser.is_open:
        # print("Closing serial")
        ser.close()
    if Config.USE_RADIO:
        if device is not None and device.is_open():
            # print("Closing radio")
            device.close()


atexit.register(exit_handler)

sender = CANSender(sio, CANframes)  # from send_from_can.py

isRunning = False

# remove rpm
# discharge -> current
# make motor faults longer/ all faults
# white mode

queue = Queue()


def read_serial():
    while True:
        try:
            encoded_message = ser.read(1)
            start_byte = int.from_bytes(encoded_message, "big")  # Checks for start byte as int for beginning of message
            # print(f"got byte: {encoded_message}")
            if start_byte == 249:  # 249 is the start message byte
                encoded_message += ser.read(24)
                # print(f"put {encoded_message} into queue")
                queue.put(encoded_message)
                if queue.qsize() > 50:
                    with queue.mutex:
                        # print("cleared queue")
                        queue.queue.clear()
        except:
            pass


def sendData():
    device = None
    while True:
        encoded_message = queue.get(block=True)
        # print(f"read {encoded_message} from queue")
        try:
            sender.send(encoded_message)  # Send data to be parsed to CAN
        except:
            pass
        try:
            if Config.USE_RADIO:
                if device is not None and device.is_open():
                    # print("Closing radio")
                    device.close()
                device = None
                device = XBeeDevice("/dev/radio", 9600)
                device.open()
                device.send_data_broadcast(encoded_message)  # Send over radio to Telemetry
        except:
            pass
        sio.sleep(0.01)


@sio.event
def connect(sid, environ):
    global isRunning, sio
    if not isRunning:
        isRunning = True
        threading.Thread(target=read_serial).start()
        sio.start_background_task(sendData)


time_received = False
if __name__ == '__main__':
    # pit starts by looping time messages
    # Car comes on, receives time message
    # Sends acknowledgement
    # Pit receives ack, sends back ack
    # Car receives ack and starts transmitting data
    if Config.USE_RADIO:
        # with open(logfilename, "w") as outfile:
        #     outfile.write("setting up callback")


        def time_handler(msg):
            global time_received
            if time_received:
                return
            msgtxt: str = msg.data.decode("utf8")
            if msgtxt.startswith("Time:"):
                seconds = int(msgtxt[5:]) - 60*60
                os.system(f"sudo date -s '@{seconds}'")
                time_received = True
                device.del_data_received_callback(time_handler)
                device.send_data_broadcast("ack")


        device.add_data_received_callback(time_handler)

        # print("start time ack loop")
        end_time = time.time() + 15
        while not time_received and time.time() <= end_time:
            pass

        if Config.USE_RADIO:
            if device is not None and device.is_open():
                # print("Closing radio")
                device.close()
                device = None
                
    eventlet.wsgi.server(eventlet.listen(('localhost', 5050)), app)
