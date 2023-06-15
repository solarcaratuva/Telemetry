#Runs on the PI, takes data off ECU board over UART, parses CAN and publishes to server
import atexit
import os
import serial,time
import cantools
import eventlet
import socketio

from send_from_can import CANSender, get_xbee_connection

# XBee Mac addresses
# pit - 0013A20041C4ACC3
# car - 0013A20041C4AC5F

#USB port on PI (UART splitter)
ser = serial.Serial("/dev/ttyUSB0",9600)
sio = socketio.Server(cors_allowed_origins=["http://localhost:3000"])
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
             "SolarCurrent": ["total_current"],
             "BPSCellTemperature": ["high_temperature"],
             "ECUPowerAuxCommands": ['hazards', 'brake_lights', 'headlights', 'left_turn_signal', 'right_turn_signal'],
             "ECUMotorCommands": ['throttle', "forward_en", "reverse_en"]
             }


device = get_xbee_connection()


def exit_handler():
    # print("Closing serial port")
    # ser.close()
    if device is not None and device.is_open():
        device.close()


atexit.register(exit_handler)

sender = CANSender(sio, CANframes) #from send_from_can.py

isRunning = False


# remove rpm
# discharge -> current
# make motor faults longer/ all faults
# white mode

def sendData():
    while True:
        encoded_message = ser.read(1)
        start_byte = int.from_bytes(encoded_message,"big") #Checks for start byte as int for beginning of message
        if(start_byte == 249): #249 is the start message byte
            encoded_message += ser.read(24) #read rest of 25 byte message
            sender.send(encoded_message) #Send data to be parsed to CAN
            device.send_data_broadcast(encoded_message) #Send over radio to Telemetry
            sio.sleep(1)


@sio.event
def connect(sid, environ):
    global isRunning, sio
    if not isRunning:
        isRunning = True
        sio.start_background_task(sendData)

time_received = False
if __name__ == '__main__':
    while True:
        encoded_message = ser.read(1)
        start_byte = int.from_bytes(encoded_message,"big") #Checks for start byte as int for beginning of message
        if(start_byte == 249): #249 is the start message byte
            encoded_message += ser.read(24) #read rest of 25 byte message
            sender.send(encoded_message) #Send data to be parsed to CAN
            #device.send_data_broadcast(encoded_message) #Send over radio to Telemetry
            sio.sleep(1)
    # pit starts by looping time messages
    # Car comes on, recieves time message
    # Sends acknnoledgement
    # Pit receives ack, sneds back ack
    # Car recives ack and starts transmitting data
    def time_handler(msg):
        global time_received
        if time_received:
            return
        msgtxt: str = msg.data.decode("utf8")
        if msgtxt.startswith("Time:"):
            seconds = int(msgtxt[5:])
            os.system(f"sudo date -s '@{seconds}'")
            time_received = True
            #device.del_data_received_callback(time_received)
            #device.send_data_broadcast("ack")


    #device.add_data_received_callback(time_handler)
    while not time_received:
        pass
    exit(0)
    eventlet.wsgi.server(eventlet.listen(('localhost', 5050)), app)
