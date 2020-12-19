from flask import render_template 
from app import app, db, runTracker, basic_auth 

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