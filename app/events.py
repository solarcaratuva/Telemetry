from app import db, socketio, runTracker, randData
from .models import Base, BMS, KLS, Runs, TestData
from .data_handler import storeData
import msgpack
from sqlalchemy import desc
#SocketIO Events
#Restore data on connect/refresh
@socketio.on('connect')
def handle_connect():
    if(runTracker.isRecording()):
        pass 
        data_json = db.session.query(BMS.json).filter_by(run_id=runTracker.getID()).all()
        socketio.emit('restoreData', data_json)

#Emit data for given run_id
@socketio.on('loadData')
def load_data(run_id):
    print("Loading run #" + str(run_id))

    data_json = db.session.query(BMS.json).filter_by(run_id=run_id).all()
    print(data_json)
    socketio.emit('loadData', data_json)

#Create and start new run
@socketio.on('new_run')
def create_run(run):
    run = Runs(title=run['title'], 
               driver=run['driver'], 
               location=run['location'], 
               description=run['description'])
    
    if run.title.strip() == '':
        run.title = 'Unnamed Run {}'.format(run.run_id)

    db.session.add(run)
    db.session.commit()
    print("COMMITED NEW RUN SESSION YEET:", run.run_id)

    runID = run.run_id
    runTracker.startRun(runID)
    print("Starting run " + str(runID))

    socketio.emit('toggleRecording')
    emit_data()

#Stop current run
@socketio.on('stop_run')
def stop_run():
    runTracker.stopRun()
    print("Stopped run #" + str(runTracker.getID()))
    socketio.emit('toggleRecording')

@socketio.on('connect_run')
def connect_run(run):
    runTracker.viewRun(int(run['run_id']))
    emit_data()

#Loop to emit data to client
def emit_data():
    while runTracker.isViewing():
        print("HELL YEAH YAM RECORDING")
        print("Emit runID ", runTracker.getID())

        #info = data.Info().to_json()
        # randData.gen_random()
        # TODO: Test out descending
        data_obj = db.session.query(TestData).filter_by(run_id=runTracker.getID()).order_by(desc(TestData.timestamp)).limit(1).one()
        keys = [i for i in vars(data_obj) if not i.startswith('_')]
        data_json = {}
        for key in keys:
            data_json[key] = data_obj.__dict__[key]
        print(keys)
        print(data_json)
        socketio.emit('dataEvent', data_json)
        socketio.sleep(1)