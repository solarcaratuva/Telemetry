import time

from digi.xbee.devices import XBeeDevice, RemoteXBeeDevice
import serial.tools.list_ports
from digi.xbee.models.address import XBee64BitAddress

PORT = "COM4"
# TODO: Replace with the port where your local module is connected to.
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600

# TODO: Replace with the 64-bit address of the remote device.
REMOTE_DEVICE_ADDRESS = "0013A20041C4ACC3"


def main():
    local_device = XBeeDevice(PORT, BAUD_RATE)

    try:
        local_device.open()

        # Instantiate a remote XBee device object to send data.
        # remote_device = RemoteXBeeDevice(local_device, XBee64BitAddress.from_hex_string(REMOTE_DEVICE_ADDRESS))
        while True:
            local_device.send_data_broadcast("hi world")
            time.sleep(1)
        # Send data using the remote object.
        # local_device.send_data(remote_device, "Hello XBee!")

        print("Data sent successfully")

    finally:
        if local_device is not None and local_device.is_open():
            local_device.close()


if __name__ == "__main__":
    main()
