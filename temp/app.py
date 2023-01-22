from flask import Flask, render_template
from flask_socketio import SocketIO
from random import randint
import time
from datetime import datetime

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
    socket.send("pedal_value", {timestamp: current_date.isoformat(), number: 50})
    print("send date")

# Running app
if __name__ == '__main__':
    socket.run(app, port=5050, allow_unsafe_werkzeug=True)
