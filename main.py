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

#XBee
useSerial = False
PORT = "COM3"
BAUD_RATE = 9600

Payload.max_decode_packets = 5000
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

#Authentication
app.config['BASIC_AUTH_USERNAME'] = 'byoon'
app.config['BASIC_AUTH_PASSWORD'] = '123'
#app.config['BASIC_AUTH_FORCE'] = True
basic_auth = BasicAuth(app)

socketio = SocketIO(app)

#Serial Ports
#serial_port = 'ttyS11'
#ser = serial.Serial(serial_port, 115200, timeout=1)

'''
    def __repr__(self):
        return f"Data:('{self.miles}', '{self.rpm}', '{self.mph}')"
'''

db.create_all()

class RunTracker(object):
    def __init__(self):
        self.runID = None
        self.recording = False

    def startRun(self, runID):
        self.runID = runID
        self.recording = True

    def stopRun(self):
        self.runID = None
        self.recording = False

    def getID(self):
        return self.runID

    def isRecording(self):
        return self.recording

runTracker = RunTracker()

#Routes
@app.route('/')
def sessions():
    recording = runTracker.isRecording()
    return render_template('index.html', recording=recording)

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

@app.route('/layout')
def layout():
    return render_template('layout.html')

@app.route('/admin')
@basic_auth.required
def secret_view():
    return render_template('admin.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/load')
def load_run():
    runs_list = db.session.query(Runs).all()
    return render_template('load.html', runs_list = runs_list)

@app.route('/test')
def submit():
    runs_list = db.session.query(Runs).all()
    recording = runTracker.isRecording()
    return render_template('test.html', runs_list = runs_list, recording = recording)

#API endpoint for getting random json data
@app.route('/data', methods = ['GET'])
def getData():
        info = data.Info().to_json()
        data_json = msgpack.unpackb(info, raw=False)
        return data_json

#endpoint for getting current run id
@app.route('/id')
def get_id():
    id = runTracker.getID()
    return str(id)

#endpoint for stopping current run
@app.route('/stop')
def stop_recording():    
    runTracker.stopRun()
    return render_template('test.html', runs_list = db.session.query(Runs).all()
)
    

#SocketIO Events
#Restore data on connect/refresh
@socketio.on('connect')
def handle_connect():
    if(runTracker.isRecording()):
        data_json = db.session.query(BMS.json).filter_by(run_id=runTracker.getID()).all()
        socketio.emit('restoreData', data_json)

#Emit data for given run_id
@socketio.on('loadData')
def load_data(run_id):
    print("Loading run #" + str(run_id))

    data_json = db.session.query(BMS.json).filter_by(run_id=run_id).all()
    socketio.emit('loadData', data_json)

#Create and start new run
@socketio.on('new_run')
def create_run(run):
    run = Runs(title=run['title'], 
               driver=run['driver'], 
               location=run['location'], 
               description=run['description'])

    db.session.add(run)
    db.session.commit()

    runID = runTracker.startRun(run.run_id)
    print("Starting run " + str(runID))

    socketio.emit('toggleRecording')
    emit_data()

#Stop current run
@socketio.on('stop_run')
def stop_run():
    runTracker.stopRun()
    print("Stopped run #" + str(runTracker.getID()))
    socketio.emit('toggleRecording')

#Loop to emit data to client
def emit_data():
        while(runTracker.isRecording()):
            print("Emit runID " + str(runTracker.getID()))

            info = data.Info().to_json()
            data_json = msgpack.unpackb(info, raw=False)
            storeData(data_json)

            socketio.emit('dataEvent', data_json)
            socketio.sleep(1)

#Store data in db
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
                    run_id = runTracker.getID(),
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
                    run_id = runTracker.getID()
                    )

    db.session.add(BMS_data)
    db.session.add(KLS_data)
    db.session.commit()


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
