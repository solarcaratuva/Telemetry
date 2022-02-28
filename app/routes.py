from sqlalchemy import desc
from flask import render_template, request
from app import app, basic_auth
from .models import Runs
from .events import emit_data

#Routes
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
    return render_template('test.html', runs_list=runs_list)

#API endpoint for getting json data
# TODO: Implement this?
@app.route('/data', methods = ['GET'])
def getData():
    return None

#API endpoint for updating the json data
# TODO: Update this to take in actual data instead of just generating random data
@app.route('/update', methods = ['POST'])
def updateData():
    if request.method == 'POST':
        print("Emitting data!")
        emit_data()
        return ('', 204)

#endpoint for getting the latest run id
@app.route('/id')
def get_id():
    latest_run = Runs.query.order_by(desc(Runs.timestamp)).first()
    if latest_run is None:
        return "No runs found"
    else:
        return str(latest_run.run_id)
