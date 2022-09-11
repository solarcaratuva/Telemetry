import socketio

sio = socketio.Server()

app = socketio.WSGIApp(sio)

num = 9


@sio.event
def nums(num):
    pass