import serial
from send_from_can import *
from decode_can_dbc import *


def decode_fault_codes(raw_data):
    # Define the fault codes based on their bit positions
    fault_codes = {
        0: "internal_communications_fault",
        1: "internal_conversion_fault",
        2: "weak_cell_fault",
        3: "low_cell_voltage_fault",
        4: "open_wiring_fault",
        5: "current_sensor_fault",
        6: "pack_voltage_sensor_fault",
        7: "weak_pack_fault",
        8: "voltage_redundancy_fault",
        9: "fan_monitor_fault",
        10: "thermistor_fault",
        11: "CANBUS_communications_fault",
        12: "always_on_supply_fault",
        13: "high_voltage_isolation_fault",
        14: "power_supply_12v_fault",
        15: "charge_limit_enforcement_fault",
        16: "discharge_limit_enforcement_fault",
        17: "charger_safety_relay_fault",
        18: "internal_memory_fault",
        19: "internal_thermistor_fault",
        20: "internal_logic_fault"
    }

    active_faults = []

    # Check each fault bit if it is set
    for bit_position, fault_name in fault_codes.items():
        if raw_data & (1 << bit_position):  # Shift 1 left by bit_position and check with AND
            active_faults.append(fault_name)

    return active_faults

ser = serial.Serial(port="COM10", baudrate=9600)

pack_voltage = 0
pack_current = 0
motor_rpm = 0
high_cell_tmp = 0
regen = 0
cruise_control_speed = 0
cruise_control_en = 0

curr_faults = []

while True:
    try:
        curr_msg = ser.readline().decode('utf-8')[:-1].split()
        msg_id = curr_msg[0]

        if msg_id == "pack_voltage":
            pack_voltage = float(curr_msg[1])/100
        elif msg_id == "pack_current":
            pack_current = float(curr_msg[1])/10
        elif msg_id == "motor_rpm":
            motor_rpm = int(curr_msg[1])
        elif msg_id == "tmp":
            high_cell_tmp = int(curr_msg[1])
        elif msg_id == "regen":
            regen = int(curr_msg[1])
        elif msg_id == "cc_speed":
            cruise_control_speed = int(curr_msg[1])
        elif msg_id == "cc_en":
            cruise_control_en = int(curr_msg[1])
        elif msg_id == "bms_fault":
            bms_fault_in = int(curr_msg[1])
            curr_faults = decode_fault_codes(bms_fault_in)

        # print(encoded_message)
        #
        # start_byte = int.from_bytes(encoded_message, "big")  # Checks for start byte as int for beginning of message
        # # print(f"got byte: {start_byte}")
        # if start_byte == 249:  # 249 is the start message byte
        #     encoded_message += ser.read(24)
        #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        #     print(f"encoded message: {encoded_message}")
        #     ints = []
        #     for byte in encoded_message:
        #         ints.append(byte)
        #     message_id = int.from_bytes(encoded_message[1:3], "big")  # first two bytes are message id
        #     print(f"id: {message_id}")
        #     # print(f"message id: {message_id}")
        #     message_body = encoded_message[3:17]
        #     print(f"message body: {message_body}")
        #     m = make_hex_great_again(message_body)
        #     print(f"after make hex: {m}")
        #     print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            # print(encoded_message)
            # name, values = get_can_data(encoded_message)
            # if name == "BPSPackInformation":
            #     pack_current = values["pack_current"]
            #     print("~~~~~~~~~~~~~~~~~~~~~~~")
            #     if len(curr_faults) > 0:
            #         for fault in curr_faults:
            #             print(fault)
            #     else:
            #         print("No faults")
            #     print(f"pack_current: {pack_current}")
            #     print("~~~~~~~~~~~~~~~~~~~~~~~")
            # elif name in ("BPSError", "MotorControllerError", "PowerAuxError"):
            #     curr_faults = []
            #     for k, v in values.items():
            #         if v == 1:
            #             curr_faults.append(k)
            #     print("~~~~~~~~~~~~~~~~~~~~~~~")
            #     if len(curr_faults) > 0:
            #         for fault in curr_faults:
            #             print(fault)
            #     else:
            #         print("No faults")
            #     print(f"pack_current: {pack_current}")
            #     print("~~~~~~~~~~~~~~~~~~~~~~~")
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
