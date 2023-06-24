import time

from send_from_can import get_xbee_connection

ack_received = False
if __name__ == '__main__':
    device = get_xbee_connection()
    def ack_handler(msg):
        global ack_received
        print("acked")
        if msg.data.decode("utf8") == "ack":
            ack_received = True
            device.del_data_received_callback(ack_received)


    device.add_data_received_callback(ack_handler)
    while not ack_received:
        sending = f"Time:{int(time.time())}"
        device.send_data_broadcast(sending)
        print(f"sent: {sending}")
        time.sleep(2)
