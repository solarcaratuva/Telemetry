import socketio
import math
import random 

sio = socketio.Server()

app = socketio.WSGIApp(sio)

num = random.random()*100 + 1 


@sio.event
def nums(num):
    pass