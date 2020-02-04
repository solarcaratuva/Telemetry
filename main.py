from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import data
import json
from engineio.payload import Payload
#from digi.xbee.devices import XBeeDevice

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
    data_json = data.Info().to_json()
    socketio.sleep(2)

    with open('data.txt', 'a') as file:
        file.write(json.dumps(data_json))
        file.write('\n')

    socketio.emit('dataEvent', data_json)



if __name__ == '__main__':
    #readData();
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)