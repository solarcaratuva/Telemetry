from app import app, db, socketio 
from app.models import BMS, KLS, Runs 
import socket, serial
import json

# config_file = open("config.json")
# config = json.load(config_file)

# XBEE_CONNECTED = False

# if config["USE_XBEE"]:
#     ser = serial.Serial(config["XBEE_ADDR"], baudrate=config["XBEE_BAUD"])
# else:
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     sock.bind((config["SOCKET_HOST"], config["SOCKET_PORT"]))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
