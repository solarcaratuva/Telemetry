import serial, socketio, json, time

ser = serial.Serial(port="/dev/serial0")
sio = socketio.Server()

# PySerial testing
print("Listening on: "+ser.name)
while True:
    message = ser.read(100).decode('utf-8')
    print(message)
    print("MESSAGE RECIEVED")

"""
while True:
    data = serial.read(1000).decode('utf-8')
    message = decode_can_dbc(0, data)
    json = json.dumps(message)
    sio.emit("event", json)
   
    time.sleep(0.01)
"""