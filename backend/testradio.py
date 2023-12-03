from digi.xbee.devices import XBeeDevice

if __name__ == "__main__":
    device = XBeeDevice("/dev/radio", 9600)
    device.open()
    device.send_data_broadcast("test message")
