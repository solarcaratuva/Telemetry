import time

from digi.xbee.devices import XBeeDevice

import serial.tools.list_ports
from digi.xbee.exception import XBeeException


def get_xbee_connection():
    BAUD_RATE = 9600
    ports = serial.tools.list_ports.comports()

    for port in ports:
        # Try to open a connection to each port.
        try:
            device = XBeeDevice(port.device, BAUD_RATE)
            if not device.is_open():
                device.open()

            # If we get here, we've successfully opened a connection.
            # We can now try to read a parameter from the device.
            try:
                device.get_64bit_addr()
                print(f"Connecting to {port.device}")
                return device
            except:
                continue
        except:
            # Couldn't open a connection to this port. It's either in use
            # or doesn't have an XBee connected.
            pass
    return None
i = 0

def main():
    global i
    local_device = get_xbee_connection()

    try:
        # Instantiate a remote XBee device object to send data.
        # remote_device = RemoteXBeeDevice(local_device, XBee64BitAddress.from_hex_string(REMOTE_DEVICE_ADDRESS))
        while True:
            if not local_device.is_open():
                local_device.open()
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
