import atexit
import os
# import time

import cantools
import eventlet
import serial.tools.list_ports
import socketio

from send_from_can import CANSender, get_xbee_connection

# XBee Mac addresses
# 0013A20041C4ACC3
# 0013A20041C4AC5F

ports = serial.tools.list_ports.comports()
sio = socketio.Server(cors_allowed_origins=["http://localhost:3000", "http://localhost:12345"])
app = socketio.WSGIApp(sio)

curr_path = os.path.dirname(os.path.abspath(__file__))
can_dir = os.path.join(curr_path, "CAN-messages")
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
             "BPSPackInformation": ["pack_voltage", "pack_current", "is_charging_signal_status"],
             "SolarVoltage": ["panel1_voltage", "panel2_voltage", "panel3_voltage", "panel4_voltage"],
             "SolarTemp": ["panel1_temp", "panel2_temp", "panel3_temp", "panel4_temp"]
             }

device = get_xbee_connection()


def exit_handler():
    print("Closing serial port")
    if device is not None and device.is_open():
        device.close()


atexit.register(exit_handler)

sender = CANSender(sio, CANframes)

isRunning = False


# remove rpm
# discharge -> current
# make motor faults longer/ all faults
# white mode

def sendData():  # replacement for send_data
    print("LISTENING FOR DATA")

    def data_receive_callback(xbee_message):
        address = xbee_message.remote_device.get_64bit_addr()
        data = xbee_message.data#.decode("utf8")
        print("Received data from %s: %s" % (address, data))
        sender.send(data)

    device.add_data_received_callback(data_receive_callback)


@sio.event
def connect(sid, environ):
    global isRunning
    if not isRunning:
        isRunning = True
        sio.start_background_task(sendData)


ack_received = False
if __name__ == '__main__':

    # def ack_handler(msg):
    #     global ack_received
    #     print("acked")
    #     if msg.data.decode("utf8") == "ack":
    #         ack_received = True
    #         device.del_data_received_callback(ack_received)


    # device.add_data_received_callback(ack_handler)
    # while not ack_received:
    #     sending = f"Time:{int(time.time())}"
    #     device.send_data_broadcast(sending)
    #     print(f"sent: {sending}")
    #     time.sleep(2)

    eventlet.wsgi.server(eventlet.listen(('localhost', 5050)), app)
