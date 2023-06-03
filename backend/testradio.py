import time

from backend.send_from_can import get_xbee_connection

i = 0

def main():
    global i
    local_device = get_xbee_connection()

    try:
        local_device.open()

        # Instantiate a remote XBee device object to send data.
        # remote_device = RemoteXBeeDevice(local_device, XBee64BitAddress.from_hex_string(REMOTE_DEVICE_ADDRESS))
        while True:
            local_device.send_data_broadcast(f"hi world {i}")
            i += 1
            time.sleep(3)
        # Send data using the remote object.
        # local_device.send_data(remote_device, "Hello XBee!")

        print("Data sent successfully")

    finally:
        if local_device is not None and local_device.is_open():
            local_device.close()


if __name__ == "__main__":
    main()
