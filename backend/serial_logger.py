import serial
import send_from_can

ser = serial.Serial(port="/dev/canUART", baudrate=9600)

while True:
    try:
        encoded_message = ser.read(1)
        # print(encoded_message)
        #
        start_byte = int.from_bytes(encoded_message, "big")  # Checks for start byte as int for beginning of message
        # print(f"got byte: {start_byte}")
        if start_byte == 249:  # 249 is the start message byte
            encoded_message += ser.read(24)
            print(encoded_message)
            print(get_can_data(encoded_message))
    except Exception:
        print("error")

