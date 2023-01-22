from flask import Flask, render_template
from flask_socketio import SocketIO
from random import randint
import time
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = "b"
socket = SocketIO(app, cors_allowed_origins="*")

@socket.on('message')
def handle(msg):
    time.sleep(5)
    mph = randint(1,100)
    socket.send(mph)
    print("IWRHFHWGOWIHRHOHGW")

@socket.on("connect")
def connectHandle():
    print("connected")
    time.sleep(10)
    current_date = datetime.now()
    data = json.dumps({"value": 100, "timestamp": str(current_date)})
    socket.send("pedal_value", data)
    print("send date")

# Running app
if __name__ == '__main__':
    socket.run(app, port=5050, allow_unsafe_werkzeug=True)
