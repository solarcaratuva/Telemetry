from app import db, socketio, runTracker, randData
from .models import Base, BMS, KLS, Runs
from .data_handler import storeData
import msgpack
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
    print(data_json)
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

            #info = data.Info().to_json()
            info = randData.to_json()
            data_json = msgpack.unpackb(info, raw=False)
            storeData(data_json)

            socketio.emit('dataEvent', data_json)
            socketio.sleep(1)