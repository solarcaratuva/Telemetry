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


PORT = "COM3"
BAUD_RATE = 9600

Payload.max_decode_packets = 500


app = Flask(__name__)

app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///telemetry2.db'

db = SQLAlchemy(app)
socketio = SocketIO(app)


class BMS(db.Model):
    current = db.Column(db.Float, primary_key=True)
    voltage = db.Column(db.Float)
    soc = db.Column(db.Float)
    max_temperature = db.Column(INTEGER(unsigned=True))
    temperature = db.Column(INTEGER(unsigned=True))
    charge_limit = db.Column(INTEGER(unsigned=True))
    discharge_limit = db.Column(INTEGER(unsigned=True))
    current_limit = db.Column(INTEGER(unsigned=True))
    disch_bool = db.Column(db.Boolean, default = False)
    charge_bool = db.Column(db.Boolean, default = False)
    safety_bool = db.Column(db.Boolean, default = False)
    malfunction = db.Column(db.Boolean, default = False)
    multi_purpose_out = db.Column(db.Boolean, default = False)
    always_on_signal = db.Column(db.Boolean, default = False)
    ready_signal = db.Column(db.Boolean, default = False)
    charge_signal = db.Column(db.Boolean, default = False)
    P0A1F = db.Column(db.Boolean, default = False)
    P0A00 = db.Column(db.Boolean, default = False)
    P0A80 = db.Column(db.Boolean, default = False)
    P0AFA = db.Column(db.Boolean, default = False)
    U0100 = db.Column(db.Boolean, default = False)
    P0A04 = db.Column(db.Boolean, default = False)
    P0AC0 = db.Column(db.Boolean, default = False)
    P0A01 = db.Column(db.Boolean, default = False)
    P0A02 = db.Column(db.Boolean, default = False)
    P0A03 = db.Column(db.Boolean, default = False)
    P0A81 = db.Column(db.Boolean, default = False)
    P0A9C = db.Column(db.Boolean, default = False)
    P0560 = db.Column(db.Boolean, default = False)
    P0AA6 = db.Column(db.Boolean, default = False)
    P0A05 = db.Column(db.Boolean, default = False)
    P0A06 = db.Column(db.Boolean, default = False)
    P0A07 = db.Column(db.Boolean, default = False)
    P0A08 = db.Column(db.Boolean, default = False)
    P0A09 = db.Column(db.Boolean, default = False)
    P0A0A = db.Column(db.Boolean, default = False)
    P0A0B = db.Column(db.Boolean, default = False)

class KLS(db.Model):
    command_status = db.Column(db.Boolean, default = False, primary_key = True)
    feedback_status = db.Column(db.Integer)
    hall_a = db.Column(db.Boolean, default = False)
    hall_b = db.Column(db.Boolean, default = False)
    hall_c = db.Column(db.Boolean, default = False)
    brake = db.Column(db.Boolean, default = False)
    backward = db.Column(db.Boolean, default = False)
    forward = db.Column(db.Boolean, default = False)
    foot = db.Column(db.Boolean, default = False)
    boost = db.Column(db.Boolean, default = False)
    rpm = db.Column(INTEGER(unsigned=True))
    current_limit_status = db.Column(db.Float)
    voltage = db.Column(db.Float)
    throttle = db.Column(db.Float)
    controller_temp = db.Column(INTEGER(unsigned=True))
    motor_temp = db.Column(INTEGER(unsigned=True))
    timestamp = db.Column(db.DateTime, default = datetime.now)


    def __repr__(self):
        return f"Data:('{self.miles}', '{self.rpm}', '{self.mph}')"



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

@socketio.on('dataEvent')
def handle_data(msg):
    data_json = data.Info().to_json()
    storeData(data_json)
    socketio.emit('dataEvent', data_json)
    socketio.sleep(2)


def storeData(data):
    d = KLS(rpm=data['rpm'])
    db.session.add(d)
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
