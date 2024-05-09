import time
import threading
import serial
import os
from digi.xbee.devices import XBeeDevice
import atexit

import Config


def decode_fault_codes(raw_data):
    global curr_faults
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

    curr_faults = []

    # Check each fault bit if it is set
    for bit_position, fault_name in fault_codes.items():
        if raw_data & (1 << bit_position):  # Shift 1 left by bit_position and check with AND
            curr_faults.append(fault_name)


pack_voltage = 0
pack_current = 0
motor_rpm = 0
high_cell_tmp = 0
regen = 0
cruise_control_speed = 0
cruise_control_en = 0
left_turn = False
right_turn = False
curr_faults = []
other_error = False

lock = threading.Lock()

def find_serial_port() -> str:
    ports = os.listdir("/dev/serial/by-id/")
    for port in ports:
        if "usb-Teensyduino_USB_Serial" in port:
            return port


def handle_serial():

    global pack_voltage, pack_current, motor_rpm, high_cell_tmp, regen, cruise_control_speed,\
        cruise_control_en, left_turn, right_turn, other_error
    if Config.USE_RADIO:
        radio = XBeeDevice("/dev/radio", 9600)
        radio.open()
        atexit.register(lambda: radio.close())
    while True:
        try: 
            port = find_serial_port()
            if port is None:
                print("No serial port found, retrying...")
                time.sleep(1)
                continue
            ser = serial.Serial(port=port, baudrate=9600)

            while True:
                try:
                    curr_msg = ser.readline().decode('utf-8')[:-1].split()
                    if Config.USE_RADIO:
                        radio.send_data_broadcast(curr_msg)
                    msg_id = curr_msg[0]

                    with lock:
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
                            decode_fault_codes(bms_fault_in)
                        elif msg_id == "left_turn":
                            left_turn = int(curr_msg[1]) == 1
                        elif msg_id == "right_turn":
                            right_turn = int(curr_msg[1]) == 1
                        elif msg_id == "other_error":
                            other_error = int(curr_msg[1]) == 1
                except Exception as e:
                    if type(e) == serial.SerialException:
                        raise e
                    print(f"error: {e}")
        except serial.SerialException as e:
            print("Serial Port not connected, retrying...")
            time.sleep(1)


def display_info():
    while True:
        with lock:
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"pack voltage: {pack_voltage}")
            print(f"pack current: {pack_current}")
            speed_mph = (motor_rpm * 3.1415926535 * 16 * 60) / 63360
            print(f"speed: {speed_mph}")
            print(f"tmp: {high_cell_tmp}")
            print(f"regen: {'on' if regen else 'off'}")
            print(f"cc speed: {cruise_control_speed}")
            print(f"cc: {'on' if cruise_control_en else 'off'}")
            print(f"left: {'on' if left_turn else 'off'}")
            print(f"right: {'on' if right_turn else 'off'}")
            faults_list = ["other_error"] if other_error else []
            faults_list.extend(curr_faults)
            print(f"faults: {'None' if len(faults_list) == 0 else ', '.join(faults_list)}")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        time.sleep(1)


if __name__ == "__main__":
    serial_thread = threading.Thread(target=handle_serial)
    timer_thread = threading.Thread(target=display_info)

    # Start threads
    serial_thread.start()
    timer_thread.start()
