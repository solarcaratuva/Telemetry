from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import data
from engineio.payload import Payload
from digi.xbee.devices import XBeeDevice
import msgpack
import json
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.mysql import INTEGER
import pymysql
from models import Base, BMS, KLS
import serial
from flask_basicauth import BasicAuth

PORT = "COM3"
BAUD_RATE = 9600

Payload.max_decode_packets = 500


app = Flask(__name__)

app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///telemetry2.db'
db = SQLAlchemy(app)
db.Model = Base

app.config['BASIC_AUTH_USERNAME'] = 'byoon'
app.config['BASIC_AUTH_PASSWORD'] = '123'
basic_auth = BasicAuth(app)

socketio = SocketIO(app)

serial_port = 'ttyS11'
ser = serial.Serial(serial_port, 115200, timeout=1)

'''
    def __repr__(self):
        return f"Data:('{self.miles}', '{self.rpm}', '{self.mph}')"
'''


db.create_all()


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

@app.route('/faults')
def faults():
    return render_template('faults.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')


useSerial = False

@socketio.on('dataEvent')
def handle_data(msg):
    print(msg)

    if(useSerial):
        info = ser.read(104) 
    else:
        info = data.Info().to_json()

    data_json = msgpack.unpackb(info, raw=False)
    print(data_json)
    storeData(data_json)
    socketio.emit('dataEvent', data_json)
    socketio.sleep(2)


def storeData(data):
    print("CURRENT: ")
    print(data['b'][0])
    BMS_data = BMS(current=data['b'][0],
                    voltage=data['b'][1],
                    soc=data['b'][2],
                    max_temperature=data['b'][3],
                    temperature=data['b'][4],
                    charge_limit=data['b'][5],
                    discharge_limit=data['b'][6],
                    current_limit=data['b'][7],
                    disch_bool=data['c'][0],
                    charge_bool=data['c'][1],
                    safety_bool=data['c'][2],
                    malfunction=data['c'][3],
                    multi_purpose_out=data['c'][4],
                    always_on_signal=data['c'][5],
                    ready_signal=data['c'][6],
                    charge_signal=data['c'][7],
                    P0A1F=data['f'][0],
                    P0A00=data['f'][1],
                    P0A80=data['f'][2],
                    P0AFA=data['f'][3],
                    U0100=data['f'][4],
                    P0A04=data['f'][5],
                    P0AC0=data['f'][6],
                    P0A01=data['f'][7],
                    P0A02=data['f'][8],
                    P0A03=data['f'][9],
                    P0A81=data['f'][10],
                    P0A9C=data['f'][11],
                    P0560=data['f'][12],
                    P0AA6=data['f'][13],
                    P0A05=data['f'][14],
                    P0A06=data['f'][15],
                    P0A07=data['f'][16],
                    P0A08=data['f'][17],
                    P0A09=data['f'][18],
                    P0A0A=data['f'][19],
                    P0A0B=data['f'][20]
                    )

    KLS_data = KLS(command_status=data['sa'][0],
                    feedback_status=data['sa'][0],
                    hall_a=data['sa'][0],
                    hall_b=data['sb'][0],
                    hall_c=data['sc'][0],
                    brake=data['sd'][0],
                    backward=data['se'][0],
                    forward=data['sf'][0],
                    foot=data['sg'][0],
                    boost=data['sh'][0],
                    rpm=data['k'][0],
                    current_limit_status=data['k'][1],
                    voltage=data['k'][2],
                    throttle=data['k'][3],
                    controller_temp=data['k'][4],
                    motor_temp=data['k'][5],
                    )
    db.session.add(BMS_data)
    db.session.add(KLS_data)
    db.session.commit()

"""     device = XBeeDevice(PORT, BAUD_RATE)
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
            device.close() """


if __name__ == '__main__':
    device = XBeeDevice(PORT, BAUD_RATE)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
