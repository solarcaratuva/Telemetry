from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import data
from engineio.payload import Payload
from digi.xbee.devices import XBeeDevice
import msgpack
import json

PORT = "COM3"
BAUD_RATE = 9600

Payload.max_decode_packets = 500


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('index.html')

@app.route('/battery')
def battery():
    return render_template('battery.html')

@app.route('/solar')
def solar():
    return render_template('solar.html')

@app.route('/motor')
def motor():
    return render_template('motor.html')

@app.route('/control')
def control():
    return render_template('control.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@socketio.on('dataEvent')
def handle_data(msg):
    device = XBeeDevice(PORT, BAUD_RATE)
    print("Waiting for data... \n")
    try:
        device.open()

        def data_receive_callback(xbee_message):
            data2 = msgpack.unpackb(xbee_message.data, use_list = False, raw = False)
            print(data2)
            socketio.emit('dataEvent', data2)

        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    device = XBeeDevice(PORT, BAUD_RATE)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)