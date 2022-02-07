import websocket 
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600)

def on_message(wsapp, message):
    # Send message over serial
    # print(message, type(message))
    print(message)
    message = message + '\n'
    ser.write(message.encode())


wsapp = websocket.WebSocketApp("ws://localhost:8080/test", on_message=on_message)
wsapp.run_forever()
