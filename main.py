from flask import Flask, render_template
from flask_socketio import SocketIO
import random
#from gevent.pywsgi import WSGIServer


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
#http_server = WSGIServer(('127.0.0.1', 5000), app)
#http_server.serve_forever()
socketio = SocketIO(app)



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


def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')



@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    speed =0
     #input('speed: ')
    rpm =0
     #input('rpm: ')
    socketio.emit('my response', {'speed': speed, 'rpm': rpm}, callback=messageReceived)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)

