from send_from_can import get_xbee_connection

if __name__ == "__main__":
    device = get_xbee_connection()
    while True:
        msg = device.read_data(100000)
        print(f"recd {msg.data}")
