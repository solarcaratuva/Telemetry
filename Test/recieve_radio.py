import serial.tools.list_ports
from digi.xbee.devices import XBeeDevice
import time

def get_xbee_connection():
    BAUD_RATE = 9600
    ports = serial.tools.list_ports.comports()

    for port in ports:
        # Try to open a connection to each port.
        try:
            device = XBeeDevice(port.device, BAUD_RATE)
            if device.is_open():
                device.close()
            if not device.is_open():
                device.open()
            # If we get here, we've successfully opened a connection.
            # We can now try to read a parameter from the device.
            try:
                device.get_64bit_addr()
                return device, port.device
            except:
                continue
        except:
            # Couldn't open a connection to this port. It's either in use
            # or doesn't have an XBee connected.
            pass
    return None

if __name__ == "__main__":
    device, port = get_xbee_connection()
    if device is None:
        print("Couldn't find an XBee!")
    else:
        print(f"Found an XBee on {port}")
        while True:
            try:
                data = device.read_data()
                print(f"Received data: {data}")
                time.sleep(0.5)
            except KeyboardInterrupt:
                device.close()
                print("Closed connection.")