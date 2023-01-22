from flask import Flask, render_template
from flask_socketio import SocketIO
from random import randint
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = "b"
socket = SocketIO(app)

# Route for seeing a data
@app.route("/")
def main():
    return render_template("index.html")

@socket.on('message')
def handle(msg):
    time.sleep(5)
    mph = randint(1,100)
    socket.send(mph)
    print("IWRHFHWGOWIHRHOHGW")

# Running app
if __name__ == '__main__':
    socket.run(app)