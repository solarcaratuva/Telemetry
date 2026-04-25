import serial
import serial.tools.list_ports
import time
import sys
import os

BAUD = 9600

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
MAGENTA = "\033[95m"

LINE_CLEAR = "\033[2K"
CURSOR_HOME = "\033[H"
CURSOR_HIDE = "\033[?25l"
CURSOR_SHOW = "\033[?25h"

state = {}
last_seen = {}

def choose_port():
    ports = list(serial.tools.list_ports.comports())
    if not ports:
        print("No serial ports found.")
        sys.exit(1)

    print("\nAvailable ports:")
    for i, p in enumerate(ports):
        print(f"[{i}] {p.device} - {p.description}")

    idx = int(input("Select port #: "))
    return ports[idx].device

def cobs_decode(data):
    output = bytearray()
    i = 0

    while i < len(data):
        code = data[i]
        if code == 0:
            return None
        i += 1

        for _ in range(code - 1):
            if i >= len(data):
                return None
            output.append(data[i])
            i += 1

        if code < 0xFF and i < len(data):
            output.append(0)

    return bytes(output)

def hex_bytes(p):
    return " ".join(f"{b:02X}" for b in p)

def extract_le(payload, start_bit, length):
    raw = int.from_bytes(payload, "little")
    return (raw >> start_bit) & ((1 << length) - 1)

def extract_be(payload, start_bit, length):
    # DBC Motorola/endian helper for the BPS fields.
    bits = []
    for byte in payload:
        for bit in range(7, -1, -1):
            bits.append((byte >> bit) & 1)

    value = 0
    for i in range(length):
        value = (value << 1) | bits[start_bit + i]
    return value

def decode_aux(p):
    if len(p) < 3:
        return "bad length"
    aux_mv = extract_le(p, 0, 16)
    percent = extract_le(p, 16, 8)
    return f"aux_voltage={aux_mv} mV ({aux_mv / 1000:.2f} V), percent_full={percent}"

def decode_motor_commands(p):
    if len(p) < 4:
        return "bad length"

    regen = extract_le(p, 0, 9)
    cruise_speed = extract_le(p, 9, 7)
    throttle = extract_le(p, 16, 9)
    manual = extract_le(p, 25, 1)
    regen_drive = extract_le(p, 26, 1)
    cruise_drive = extract_le(p, 27, 1)

    return (
        f"regen={regen}/256 ({regen * 100 / 256:.1f}%), "
        f"cruise_speed={cruise_speed} mph, "
        f"throttle={throttle}/256 ({throttle * 100 / 256:.1f}%), "
        f"manual={manual}, regen_drive={regen_drive}, cruise_drive={cruise_drive}"
    )

def decode_dashboard(p):
    if len(p) < 1:
        return "bad length"
    b = p[0]
    return (
        f"hazards={(b >> 0) & 1}, left={(b >> 1) & 1}, right={(b >> 2) & 1}, "
        f"regen_en={(b >> 3) & 1}, cruise_inc={(b >> 4) & 1}, "
        f"cruise_en={(b >> 5) & 1}, cruise_dec={(b >> 6) & 1}, "
        f"charging_mode={(b >> 7) & 1}"
    )

def decode_heartbeat(p):
    if len(p) < 1:
        return "bad length"
    return f"source={p[0]}"

def decode_pedal(p):
    if len(p) < 3:
        return "bad length"

    throttle = extract_le(p, 0, 12)
    brake = extract_le(p, 12, 12)

    return (
        f"throttle_pedal={throttle}/4095 ({throttle * 100 / 4095:.1f}%), "
        f"brake_pedal={brake}/4095 ({brake * 100 / 4095:.1f}%)"
    )

def decode_precharge(p):
    if len(p) < 7:
        return "bad length"

    motor_stage = extract_le(p, 0, 3)
    mppt_stage = extract_le(p, 3, 3)
    cont12_fault = extract_le(p, 6, 1)
    other_fault = extract_le(p, 7, 1)
    threshold = extract_le(p, 8, 12)
    cont12 = extract_le(p, 20, 12)
    hall_motor = extract_le(p, 32, 12)
    hall_mppt = extract_le(p, 44, 12)

    return (
        f"motor_stage={motor_stage}, mppt_stage={mppt_stage}, "
        f"cont12_fault={cont12_fault}, other_fault={other_fault}, "
        f"threshold={threshold}, cont12={cont12}, "
        f"hall_motor={hall_motor}, hall_mppt={hall_mppt}"
    )

def decode_contactor_error(p):
    if len(p) < 1:
        return "bad length"
    return f"cont12_went_low={p[0] & 1}"

def decode_bps_status(p):
    if len(p) < 6:
        return "bad length"

    # FIXED decode (big-endian byte order, matches your actual data)
    pack_voltage_raw = (p[0] << 8) | p[1]
    pack_current_raw = (p[2] << 8) | p[3]
    pack_soc_raw = p[4]

    pack_voltage = pack_voltage_raw * 0.1
    pack_current = pack_current_raw * 0.1
    pack_soc = pack_soc_raw * 0.5

    flags = p[5]

    return (
        f"pack_voltage={pack_voltage:.1f} V, "
        f"pack_current={pack_current:.1f} A, "
        f"soc={pack_soc:.1f}%, "
        f"discharge_relay={flags & 1}, "
        f"charge_relay={(flags >> 1) & 1}, "
        f"charger_safety={(flags >> 2) & 1}, "
        f"charge_power={(flags >> 3) & 1}, "
        f"balancing={(flags >> 4) & 1}"
    )
    
    
def decode_bps_error(p):
    if len(p) < 2:
        return "bad length"

    raw = int.from_bytes(p[:2], "little")
    names = [
        "internal_cell_comm",
        "weak_cell",
        "low_cell_voltage",
        "cell_open_wiring",
        "thermistor",
        "current_sensor",
        "weak_pack",
        "can_comm",
        "redundant_power",
        "hv_isolation",
        "charge_enable_relay",
        "discharge_enable_relay",
        "internal_conversion",
        "internal_memory",
        "internal_thermistor",
        "internal_logic",
    ]

    active = [names[i] for i in range(16) if raw & (1 << i)]
    return "active=" + (", ".join(active) if active else "none")

def decode_mg_status(prefix):
    def inner(p):
        if len(p) < 8:
            return "bad length"
        current_ma = int.from_bytes(p[0:4], "little", signed=True)
        voltage_v = int.from_bytes(p[4:8], "little", signed=True)
        return f"{prefix}_input_current={current_ma} mA, {prefix}_input_voltage={voltage_v} V"
    return inner

def decode_mg_power(prefix):
    def inner(p):
        if len(p) < 8:
            return "bad length"
        output_v = int.from_bytes(p[0:4], "little", signed=True)
        input_power_mw = int.from_bytes(p[4:8], "little", signed=True)
        return f"{prefix}_output_voltage={output_v} V, {prefix}_input_power={input_power_mw} mW ({input_power_mw / 1000:.1f} W)"
    return inner

def decode_mg_temp(prefix):
    def inner(p):
        if len(p) < 4:
            return "bad length"
        pcb = int.from_bytes(p[0:2], "little", signed=True) * 0.01
        mosfet = int.from_bytes(p[2:4], "little", signed=True) * 0.01
        return f"{prefix}_pcb_temp={pcb:.2f} C, {prefix}_mosfet_temp={mosfet:.2f} C"
    return inner

def decode_motor_power_status(p):
    if len(p) < 8:
        return "bad length"

    battery_voltage = extract_le(p, 0, 10) * 0.5
    battery_current = extract_le(p, 10, 9)
    current_dir = extract_le(p, 19, 1)
    motor_current = extract_le(p, 20, 10)
    fet_temp = extract_le(p, 30, 5) * 5
    motor_rpm = extract_le(p, 35, 12)
    pwm_duty = extract_le(p, 47, 10) * 0.5
    lead_angle = extract_le(p, 57, 7) * 0.5

    return (
        f"battery_voltage={battery_voltage:.1f} V, battery_current={battery_current} A, "
        f"current_dir={current_dir}, motor_current={motor_current} A, "
        f"fet_temp={fet_temp} C, rpm={motor_rpm}, pwm_duty={pwm_duty:.1f}%, "
        f"lead_angle={lead_angle:.1f} deg"
    )

def decode_motor_drive_status(p):
    if len(p) < 5:
        return "bad length"

    power_mode = extract_le(p, 0, 1)
    control_mode = extract_le(p, 1, 1)
    accel = extract_le(p, 2, 10) * 0.5
    regen = extract_le(p, 12, 10) * 0.5
    digital_sw = extract_le(p, 22, 4)
    target = extract_le(p, 26, 10) * 0.5
    motor_status = extract_le(p, 36, 2)
    regen_status = extract_le(p, 38, 1)

    return (
        f"power_mode={power_mode}, control_mode={control_mode}, "
        f"accelerator={accel:.1f}, regen={regen:.1f}, digital_sw={digital_sw}, "
        f"target={target:.1f}, motor_status={motor_status}, regen_status={regen_status}"
    )

def decode_motor_error(p):
    if len(p) < 5:
        return "bad length"

    raw = int.from_bytes(p[:5], "little")
    fields = {
        0: "analog_sensor",
        1: "motor_current_u",
        2: "motor_current_w",
        3: "fet_thermistor",
        5: "battery_voltage_sensor",
        6: "battery_current_sensor",
        7: "battery_current_sensor_adj",
        8: "motor_current_sensor_adj",
        9: "accelerator_position",
        11: "controller_voltage_sensor",
        16: "power_system",
        17: "overcurrent",
        19: "overvoltage",
        21: "overcurrent_limit",
        24: "motor_system",
        25: "motor_lock",
        26: "hall_sensor_short",
        27: "hall_sensor_open",
    }

    active = [name for bit, name in fields.items() if raw & (1 << bit)]
    overheat = extract_le(p, 32, 2)

    return f"active={', '.join(active) if active else 'none'}, overheat_level={overheat}"

DECODERS = {
    0x064: ("AuxBatteryStatus", decode_aux),
    0x0C8: ("MotorCommands", decode_motor_commands),
    0x12C: ("DashboardCommands", decode_dashboard),
    0x190: ("Heartbeat", decode_heartbeat),
    0x1F4: ("PedalStatus", decode_pedal),
    0x258: ("PrechargeStatus", decode_precharge),
    0x2BC: ("Contactor12Error", decode_contactor_error),

    0x3AA: ("BpsError", decode_bps_error),
    0x406: ("BpsStatus", decode_bps_status),

    0x180: ("MG0Status", decode_mg_status("MG0")),
    0x181: ("MG1Status", decode_mg_status("MG1")),
    0x280: ("MG0OutputVoltageInputPower", decode_mg_power("MG0")),
    0x281: ("MG1OutputVoltageInputPower", decode_mg_power("MG1")),
    0x480: ("MG0PCBMOSFETTemperature", decode_mg_temp("MG0")),
    0x481: ("MG1PCBMOSFETTemperature", decode_mg_temp("MG1")),

    0x325: ("MotorControllerPowerStatus", decode_motor_power_status),
    0x315: ("MotorControllerDriveStatus", decode_motor_drive_status),
    0x115: ("MotorControllerError", decode_motor_error),
    0x332: ("MotorControllerFrameRequest", lambda p: f"power_status={p[0] & 1}, drive_status={(p[0] >> 1) & 1}, error={(p[0] >> 2) & 1}" if p else "bad length"),
}

ORDER = [
    0x190, 0x12C, 0x0C8, 0x1F4, 0x064,
    0x406, 0x3AA,
    0x258, 0x2BC,
    0x325, 0x315, 0x115, 0x332,
    0x180, 0x181, 0x280, 0x281, 0x480, 0x481,
]

def decode_packet(msg_id, payload):
    name, decoder = DECODERS.get(msg_id, (f"Unknown 0x{msg_id:03X}", None))
    decoded = decoder(payload) if decoder else f"raw={hex_bytes(payload)}"

    state[msg_id] = {
        "name": name,
        "payload": payload,
        "decoded": decoded,
        "updated": time.strftime("%H:%M:%S"),
    }
    last_seen[msg_id] = time.time()

def line_for(msg_id):
    if msg_id not in state:
        return f"{DIM}0x{msg_id:03X} waiting...{RESET}"

    e = state[msg_id]
    age = time.time() - last_seen[msg_id]

    if age < 1.0:
        age_color = GREEN
    elif age < 3.0:
        age_color = YELLOW
    else:
        age_color = RED

    return (
        f"{BOLD}0x{msg_id:03X}{RESET} "
        f"{MAGENTA}{e['name']:<32}{RESET} "
        f"{DIM}raw:{RESET} {hex_bytes(e['payload']):<24} "
        f"{age_color}{age:4.1f}s{RESET}\n"
        f"    {e['decoded']}"
    )

def render():
    lines = []
    lines.append(f"{BOLD}{CYAN}Solar Car CAN Radio Monitor{RESET}  {DIM}{time.strftime('%H:%M:%S')} | Ctrl+C to exit{RESET}")
    lines.append("")

    shown = set()
    for msg_id in ORDER:
        lines.append(line_for(msg_id))
        shown.add(msg_id)

    unknowns = sorted(k for k in state.keys() if k not in shown)
    if unknowns:
        lines.append("")
        lines.append(f"{BOLD}{YELLOW}Other / unknown messages{RESET}")
        for msg_id in unknowns:
            lines.append(line_for(msg_id))

    output = "\n".join(LINE_CLEAR + line for line in lines)
    sys.stdout.write(CURSOR_HOME + output)
    sys.stdout.flush()

def print_packet(data):
    if len(data) < 2:
        return

    msg_id = (data[0] << 8) | data[1]
    payload = data[2:]

    decode_packet(msg_id, payload)
    render()

def main():
    port = choose_port()
    ser = serial.Serial(port, BAUD, timeout=0.1)

    print(CURSOR_HIDE, end="")
    print("\n" * 45)
    print(CURSOR_HOME, end="")
    print(f"Listening on {port} @ {BAUD} baud...")

    buffer = bytearray()

    while True:
        data = ser.read(64)
        if not data:
            render()
            continue

        for b in data:
            if b == 0:
                if buffer:
                    decoded = cobs_decode(buffer)
                    if decoded:
                        print_packet(decoded)
                buffer.clear()
            else:
                buffer.append(b)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(CURSOR_SHOW)
        print("\nExiting.")