from backend.send_from_can import get_xbee_connection


def main():
    device = get_xbee_connection()

    try:

        def data_receive_callback(xbee_message):
            address = xbee_message.remote_device.get_64bit_addr()
            data = xbee_message.data.decode("utf8")
            print("Received data from %s: %s" % (address, data))

        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")
        input()

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == "__main__":
    main()
