from app import db, socketio
from .models import Runs, TestData
from sqlalchemy import desc

#SocketIO Events
#Restore data on connect/refresh
@socketio.on('connect')
def handle_connect():
    emit_data()


#Emit data for given run_id
@socketio.on('loadData')
def load_data(run_id):
    print("Loading run #" + str(run_id))

    data_json = TestData.query.filter_by(run_id=run_id).order_by(desc(TestData.timestamp)).all()
    print(data_json)
    socketio.emit('loadData', data_json)

#Loop to emit data to client
def emit_data():
    latest_run = Runs.query.order_by(desc(Runs.timestamp)).first()
    if latest_run is not None:
        latest_run_id = latest_run.run_id

        data_obj = TestData.query.filter_by(run_id=latest_run_id).order_by(desc(TestData.timestamp)).first()
        if data_obj is not None:
            keys = [i for i in vars(data_obj) if not i.startswith('_')]
            data_json = {}
            for key in keys:
                data_json[key] = data_obj.__dict__[key]
            print(keys)
            print(data_json)
            socketio.emit('dataEvent', data_json)
        