from backend.send_from_can import get_xbee_connection

device = get_xbee_connection()

device.send_data_broadcast("test")
