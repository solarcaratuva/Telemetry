# ACCESS FROM: http://localhost:5000/

from flask import Flask, render_template
from flask_socketio import SocketIO
from random import randint
import time
import json
import asyncio, serial

app = Flask(__name__)
app.config['SECRET_KEY'] = "b"
socket = SocketIO(app)
ser = serial.Serial(port="/dev/serial0")

# Route for seeing a data
@app.route("/")
def main():
    return render_template("PingPong.html")

@socket.on('message')
def handle(msg):
    message = ser.read(100)
    message = message.decode('utf-8')
    socket.send(message)
    print("MESSAGE SENT: "+message)
    time.sleep(0.1)


# Running app
if __name__ == '__main__':
    socket.run(app)