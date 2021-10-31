import websocket 

def on_message(wsapp, message):
    print(message)

wsapp = websocket.WebSocketApp("ws://localhost:8080/test", on_message=on_message)
wsapp.run_forever()
