

import time
import threading
from typing import Optional

import serial
import os
from digi.xbee.devices import XBeeDevice
import atexit

import Config

fault_codes = {
        0: "P0A1F", #"internal_communications_fault",
        1: "P0A00", #"internal_conversion_fault",
        2: "P0A80", #"weak_cell_fault",
        3: "P0AFA", #"low_cell_voltage_fault",
        4: "P0A04", #"open_wiring_fault",
        5: "P0AC0", #"current_sensor_fault",
        6: "P0A01", #"pack_voltage_sensor_fault",
        7: "P0A02", #"weak_pack_fault",
        8: "P0560", #"voltage_redundancy_fault",
        9: "P0A81", #"fan_monitor_fault",
        10: "P0A9C", #"thermistor_fault",
        11: "U0100", #"CANBUS_communications_fault",
        12: "always_on_supply_fault",
        13: "P0AA6", #"high_voltage_isolation_fault",
        14: "P0A05", #"power_supply_12v_fault",
        15: "P0A06", #"charge_limit_enforcement_fault",
        16: "P0A07", #"discharge_limit_enforcement_fault",
        17: "P0A08", #"charger_safety_relay_fault",
        18: "P0A09", #"internal_memory_fault",
        19: "P0A0A", #"internal_thermistor_fault",
        20: "P0A0B" #"internal_logic_fault"
    }

def decode_fault_codes(raw_data):
    global curr_faults_set, fault_codes
    # Define the fault codes based on their bit positions

    #curr_faults = []

    # Check each fault bit if it is set
    for bit_position, fault_name in fault_codes.items():
        if raw_data & (1 << bit_position):  # Shift 1 left by bit_position and check with AND
            #curr_faults.append(fault_name)
            curr_faults_set.add(fault_name)


pack_voltage = 0
pack_current = 0
motor_rpm = 0
high_cell_tmp = 0
regen = 0
cruise_control_speed = 0
cruise_control_en = 0
left_turn = False
right_turn = False
curr_faults_set = set()
other_error = False
hazards = False
disconnected = False

lock = threading.Lock()


def find_serial_port() -> Optional[str]:
    try:
        ports = os.listdir("/dev/serial/by-id/")
        for port in ports:
            if "usb-Teensyduino_USB_Serial" in port:
                return f"/dev/serial/by-id/{port}"
        return None
    except FileNotFoundError:
        return None


def handle_serial():

    global pack_voltage, pack_current, motor_rpm, high_cell_tmp, regen, cruise_control_speed,\
        cruise_control_en, left_turn, right_turn, other_error, hazards, disconnected
    if Config.USE_RADIO:
        radio = XBeeDevice("/dev/radio", 9600)
        radio.open()
        atexit.register(lambda: radio.close())
    while True:
        try: 
            port = find_serial_port()
            if port is None:
                print("No serial port found, retrying...")
                disconnected = True
                time.sleep(1)
                continue
            ser = serial.Serial(port=port, baudrate=9600)
            disconnected = False
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
                            new_pack_current = float(curr_msg[1])/10
                            if -50 <= new_pack_current <= 200:
                                pack_current = new_pack_current
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
                        elif msg_id == "hazards":
                            hazards = int(curr_msg[1]) == 1
                except Exception as e:
                    if type(e) == serial.SerialException:
                        raise e
                    print(f"error: {e}")
        except serial.SerialException as e:
            print("Serial Port not connected, retrying...")
            print(e)
            disconnected = True
            time.sleep(1)


def display_info():
    global curr_faults_set
    while True:
        if disconnected:
            continue
        with lock:
            lights = []
            if left_turn:
                lights.append("left_turn")
            if right_turn:
                lights.append("right_turn")
            if hazards:
                lights.append("hazards")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(f"pack voltage: {pack_voltage}")
            print(f"pack current: {pack_current}")
            speed_mph = (motor_rpm * 3.1415926535 * 16 * 60) / 63360
            print(f"speed: {int(speed_mph)}")
            print(f"tmp: {high_cell_tmp}")
            print(f"regen: {'on' if regen else 'off'}")
            print(f"cc speed: {cruise_control_speed if cruise_control_en else 0}")
            print(f"cc: {'on' if cruise_control_en else 'off'}")
            print(f"lights: {'None' if len(lights)==0 else ', '.join(lights)}")
            # print(f"left: {'on' if left_turn else 'off'}")
            # print(f"right: {'on' if right_turn else 'off'}")
            # print(f"hazards: {'on' if hazards else 'off'}")
            curr_faults = list(curr_faults_set)
            faults_list = ["other_error"] if other_error else []
            faults_list.extend(curr_faults)
            red = '\33[41m' if len(faults_list) > 0 else ''
            end = '\33[0m' if len(faults_list) > 0 else ''
            print(f"{red}faults: {'None' if len(faults_list) == 0 else ', '.join(faults_list)}{end}")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        time.sleep(1)


if __name__ == "__main__":
    serial_thread = threading.Thread(target=handle_serial)
    timer_thread = threading.Thread(target=display_info)

    # Start threads
    serial_thread.start()
    timer_thread.start()
