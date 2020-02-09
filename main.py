from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import data
from engineio.payload import Payload
from digi.xbee.devices import XBeeDevice
PORT = "COM6"
BAUD_RATE = 9600
def main():
    device = XBeeDevice(PORT, BAUD_RATE)
    print("Waiting for data... \n")
    try:
        device.open()

        def data_receive_callback(xbee_message):
            print("From %s >> %s" % (xbee_message.remote_device.get_64bit_addr(),
                                     xbee_message.data.decode()))

        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()


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

@socketio.on('dataEvent')
def handle_data(msg):
    main()
    #data_json = data.Info().to_json()
    #xbee_message = device.add_data_received_callback(data_receive_callback)
    #data = xbee_message.data
    #print(data)
    #xbee_message = input('data: ')
    #socketio.emit('dataEvent', {'mph': data })
    #socketio.emit('dataEvent', data_json)

if __name__ == '__main__':
    device = XBeeDevice(PORT, BAUD_RATE)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

