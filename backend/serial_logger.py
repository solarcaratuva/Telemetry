import serial
from send_from_can import *

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
            # print(encoded_message)
            name, values = get_can_data(encoded_message)
            if name in ("BPSError", "MotorControllerError", "PowerAuxError"):
                for k, v in values.items():
                    # if v == 1:
                    print(f"{name}: {k}: {v}")
                # errors = []
                # for data in self.can_messages[name]:
                #     if values[data]:
                #         errors.append(data)
                #
                # # print("ERRORS: " + str(errors))
                # self.sio.emit(name, {"timestamp": timestamp, "array": errors})
                # return True
    except Exception as e:
        print(f"error: {e}")

