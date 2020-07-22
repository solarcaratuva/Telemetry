from flask import Flask, render_template, request, session
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
from models import Base, BMS, KLS, Runs
import serial
from flask_basicauth import BasicAuth
from flask_session import Session
from sqlalchemy.ext.serializer import loads, dumps
from handleData import storeData


#XBee
PORT = "COM3"
BAUD_RATE = 9600

Payload.max_decode_packets = 500
app = Flask(__name__)

Runs()
#Database Setup
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
#app.config['DEBUG'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///telemetry2.db'
db = SQLAlchemy(app)
db.Model = Base

POSTGRES = {
    'user': 'postgres',
    'pw': '1234',
    'db': 'telemetry',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

app.config['BASIC_AUTH_USERNAME'] = 'byoon'
app.config['BASIC_AUTH_PASSWORD'] = '123'
basic_auth = BasicAuth(app)


#Session config
SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

socketio = SocketIO(app)

#Serial Ports
#serial_port = 'ttyS11'
#ser = serial.Serial(serial_port, 115200, timeout=1)

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

@app.route('/stop')
def stop_recording():    
    session['run_id'] = None
    return render_template('test.html', runs_list = db.session.query(Runs).all()
)

@app.route('/load')
def load_run():
    run_id = 58
    runs_list = db.session.query(Runs).all()
    BMS_data = db.session.query(BMS).filter_by(run_id=run_id)
    KLS_data = db.session.query(KLS).filter_by(run_id=run_id)
    data_json = db.session.query(BMS.json).filter_by(run_id=run_id).all()
    print(data_json)
    socketio.emit('loadData', data_json)
    load_data(run_id)
    print("--------------------------EMITTED-------------------------------------")
    return render_template('load.html', runs_list = runs_list, BMS = BMS_data, KLS = KLS_data)

@app.route('/test', methods=['GET','POST'])
def submit():
    runs_list = db.session.query(Runs).all()
    if request.method == 'POST':
        if request.form['submit'] == 'start':
            title = request.form['title']
            driver = request.form['driver']
            location = request.form['location']
            description = request.form['description']

            print(title, driver, location, description)

            run = Runs(title=title, driver=driver, location=location, description=description)
            print(type(run))
            db.session.add(run)
            db.session.commit()

            session['run_id'] = run.run_id
            print('----------------------------------------')
            print(session.get('run_id'))
            print('----------------------------------------')

            return render_template('test.html', recording=True, run=run, runs_list = runs_list)
        elif request.form['submit'] == 'stop':
            session['run_id'] = None
            return render_template('test.html', runs_list = runs_list)
    else:
        return render_template('test.html', runs_list = runs_list)


useSerial = False

@socketio.on('loadData')
def load_data(run_id):
    if(run_id != None):
        data_json = db.session.query(BMS.json).filter_by(run_id=run_id).all()
        print(data_json)
        print("**************************************************************************************************")
        socketio.emit('loadData', data_json)

@socketio.on('connectEvent')
def handle_connect(msg):
    run_id = session.get('run_id')
    print('connected' + str(run_id))
    if(run_id != None):
        data_json = db.session.query(BMS.json).filter_by(run_id=run_id).all()
        print(data_json)
        if(data_json == []):
            socketio.emit('dataEvent', 'connected')
        else:
            socketio.emit('loadData', data_json)
        socketio.sleep(5)

@socketio.on('dataEvent')
def handle_data(msg):
    #print(msg)
    if(useSerial):
        info = ser.read(104)
    else:
        info = data.Info().to_json()

    data_json = msgpack.unpackb(info, raw=False)
    #print(data_json)
    storeData(data_json)
    socketio.emit('dataEvent', data_json)
    socketio.sleep(5)

def storeData(data):
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
                    P0A0B=data['f'][20],
                    run_id = session.get('run_id'),
                    json=data
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
                    run_id = session.get('run_id')
                    )

    if(session.get('run_id') != None):
        db.session.add(BMS_data)
        db.session.add(KLS_data)
        db.session.commit()


if __name__ == '__main__':
    #print(session.get('run_id'))
    device = XBeeDevice(PORT, BAUD_RATE)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
