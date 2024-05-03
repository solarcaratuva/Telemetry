import serial
from send_from_can import *

ser = serial.Serial(port="/dev/canUART", baudrate=9600)

pack_current = 0
curr_faults = []

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
            if name == "BPSPackInformation":
                pack_current = values["pack_current"]
                print("~~~~~~~~~~~~~~~~~~~~~~~")
                if len(curr_faults) > 0:
                    for fault in curr_faults:
                        print(fault)
                else:
                    print("No faults")
                print(f"pack_current: {pack_current}")
                print("~~~~~~~~~~~~~~~~~~~~~~~")
            elif name in ("BPSError", "MotorControllerError", "PowerAuxError"):
                curr_faults = []
                for k, v in values.items():
                    if v == 1:
                        curr_faults.append(k)
                print("~~~~~~~~~~~~~~~~~~~~~~~")
                if len(curr_faults) > 0:
                    for fault in curr_faults:
                        print(fault)
                else:
                    print("No faults")
                print(f"pack_current: {pack_current}")
                print("~~~~~~~~~~~~~~~~~~~~~~~")
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

