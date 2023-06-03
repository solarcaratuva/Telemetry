from digi.xbee.devices import XBeeDevice
import serial.tools.list_ports


def get_xbee_connection():
    BAUD_RATE = 9600
    ports = serial.tools.list_ports.comports()

    for port in ports:
        # Try to open a connection to each port.
        try:
            device = XBeeDevice(port.device, BAUD_RATE)
            device.open()
            # If we get here, we've successfully opened a connection.
            # We can now try to read a parameter from the device.
            try:
                device.get_64bit_addr()
                return device
            except:
                continue
        except:
            # Couldn't open a connection to this port. It's either in use
            # or doesn't have an XBee connected.
            pass
    return None


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
