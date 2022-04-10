import msgpack
from sqlalchemy import desc
from flask import render_template, request
from app import app, db, runTracker, basic_auth, randData
from .models import Base, BMS, KLS, Runs, TestData
import csv
import json

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
    runs_list = Runs.query.order_by(Runs.run_id).all()
    return render_template('load.html', runs_list=runs_list)

@app.route('/test')
def submit():
    runs_list = Runs.query.order_by(Runs.run_id).all()
    recording = runTracker.isRecording()
    return render_template('test.html', runs_list=runs_list, recording=recording)

#API endpoint for getting json data
@app.route('/data', methods = ['GET'])
def getData():
    # print(TestData.query.order_by(desc(TestData.timestamp)).all())
    data = TestData.query.order_by(desc(TestData.timestamp)).first().__dict__
    print(data)
    data.pop("_sa_instance_state")
    return json.dumps(data)
    # return randData.data_values

#API endpoint for updating the json data
# TODO: Update this to take in actual data instead of just generating random data
@app.route('/update', methods = ['POST'])
def updateData():
    if request.method == 'POST':
        print("YEET")
        randData.gen_random()
        print("GENERATED")
        return ('', 204)


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

@app.route("/download/<int:input_run_id>")
def download(input_run_id=None):

    data = db.session.query(TestData).filter_by(run_id=input_run_id)

    result = ([([getattr(curr, column.name) for column in TestData.__mapper__.columns]) for curr in data])
    
    result = [x[0:-1] for x in result]
    print(result)


    with open('telemetry.csv', 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(result)

    # outfile = open('telemetry.csv', 'wb')
    # outcsv = csv.writer(outfile)

    # outfile.writerows(result)
    
    # [outcsv.writerow([getattr(curr, column.name) for column in BMS.__mapper__.columns]) for curr in data]
    # outcsv.writerows([x for x in data])
    # outfile.close()

    return "done"