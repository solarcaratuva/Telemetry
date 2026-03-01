import usocket as socket
import ustruct as struct
import ujson
import time
import xbee

try:
    import machine
except ImportError:
    machine = None


# ============================================================
# CONFIG
# ============================================================

AWS_ENDPOINT = "YOUR_AWS_IOT_ENDPOINT_HERE"   # e.g. abcdefg-ats.iot.us-east-1.amazonaws.com
CLIENT_ID    = "YOUR_CLIENT_ID_HERE"
TOPIC_PUB    = "telemetry/raw_json"
MQTT_PORT    = 8883

SSL_PARAMS = {
    "keyfile": "/flash/cert/private.key",
    "certfile": "/flash/cert/certificate.pem.crt",
    "server_hostname": AWS_ENDPOINT
}

# UART: you may need to change UART_PORT (0 vs 1) depending on XBee/firmware
UART_PORT = 1
UART_BAUD = 115200

# Packet format from STM32 (17 bytes):
#   START 0xA5
#   ID    uint16 little-endian
#   LEN   uint8 (0..8)
#   DATA  8 bytes
#   TS    uint32 little-endian (ms)
#   END   0x5A
START_BYTE = 0xA5
END_BYTE   = 0x5A
PKT_LEN    = 17

# Batching (publish fewer MQTT messages)
BATCH_MAX_FRAMES = 40
BATCH_FLUSH_MS   = 100   # publish at least every 100ms if any frames exist

# Retry / recovery
RETRY_MIN_MS = 500
RETRY_MAX_MS = 30000
FAIL_RESET_THRESHOLD = 50

# Safety caps
MAX_BATCH_FRAMES_HARD_CAP = 5 * BATCH_MAX_FRAMES  # prevent unbounded RAM growth
MAX_RX_BUF = 4096  # cap input buffer growth if UART floods while offline


# ============================================================
# SMALL UTILS
# ============================================================

def now_ms():
    # On MicroPython, ticks_ms is best (monotonic)
    if hasattr(time, "ticks_ms"):
        return time.ticks_ms()
    return int(time.time() * 1000)

def elapsed_ms(since):
    if hasattr(time, "ticks_diff") and hasattr(time, "ticks_ms"):
        return time.ticks_diff(time.ticks_ms(), since)
    return now_ms() - since

def sleep_ms(ms):
    if hasattr(time, "sleep_ms"):
        time.sleep_ms(ms)
    else:
        time.sleep(ms / 1000.0)

def le_u16(b0, b1):
    return (b0 & 0xFF) | ((b1 & 0xFF) << 8)

def le_u32(b0, b1, b2, b3):
    return ((b0 & 0xFF) |
            ((b1 & 0xFF) << 8) |
            ((b2 & 0xFF) << 16) |
            ((b3 & 0xFF) << 24))

def hex8(data8):
    # data8 is bytes-like length 8
    # build hex without ubinascii (works everywhere)
    return "".join(["{:02X}".format(b) for b in data8])


# ============================================================
# MQTT CLIENT (adapted from your test script)
# ============================================================

class MQTTException(Exception):
    pass

class MQTTClient:
    """A simple MQTT client for MicroPython, adapted from umqtt.simple."""
    def __init__(self, client_id, server, port=0, user=None, password=None, keepalive=60,
                 ssl=False, ssl_params=None):
        if ssl_params is None:
            ssl_params = {}
        if port == 0:
            port = 8883 if ssl else 1883
        self.client_id = client_id
        self.sock = None
        self.server = server
        self.port = port
        self.ssl = ssl
        self.ssl_params = ssl_params
        self.pid = 0
        self.cb = None
        self.user = user
        self.pswd = password
        self.keepalive = keepalive
        self.lw_topic = None
        self.lw_msg = None
        self.lw_qos = 0
        self.lw_retain = False

    def _send_str(self, s):
        if isinstance(s, str):
            s = s.encode()
        self.sock.write(struct.pack("!H", len(s)))
        self.sock.write(s)

    def _recv_len(self):
        n = 0
        sh = 0
        while 1:
            b = self.sock.read(1)[0]
            n |= (b & 0x7f) << sh
            if not b & 0x80:
                return n
            sh += 7

    def set_callback(self, f):
        self.cb = f

    def set_last_will(self, topic, msg, retain=False, qos=0):
        assert 0 <= qos <= 2
        assert topic
        self.lw_topic = topic
        self.lw_msg = msg
        self.lw_qos = qos
        self.lw_retain = retain

    def connect(self, clean_session=True):
        # XBee TLS socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_SEC)
        self.sock = xbee.wrap_socket(self.sock, **self.ssl_params)
        self.sock.connect((self.server, self.port))

        # MQTT CONNECT packet
        msg = bytearray(b"\x10\0\0\0\x04MQTT\x04\x02\0\0")
        msg[1] = 10 + 2 + len(self.client_id)
        msg[9] = clean_session << 1

        if self.user is not None:
            msg[1] += 2 + len(self.user) + 2 + len(self.pswd)
            msg[9] |= 0xC0

        if self.keepalive:
            msg[10] |= (self.keepalive >> 8) & 0xFF
            msg[11] |= self.keepalive & 0xFF

        if self.lw_topic:
            msg[1] += 2 + len(self.lw_topic) + 2 + len(self.lw_msg)
            msg[9] |= 0x4 | (self.lw_qos & 0x1) << 3 | (self.lw_qos & 0x2) << 3
            msg[9] |= self.lw_retain << 5

        self.sock.write(msg)
        self._send_str(self.client_id)

        if self.lw_topic:
            self._send_str(self.lw_topic)
            self._send_str(self.lw_msg)

        if self.user is not None:
            self._send_str(self.user)
            self._send_str(self.pswd)

        resp = self.sock.read(4)
        if resp[0] != 0x20 or resp[1] != 0x02:
            raise MQTTException("Invalid CONNACK")
        if resp[3] != 0:
            raise MQTTException("CONNACK refused: " + str(resp[3]))
        return resp[2] & 1

    def disconnect(self):
        try:
            self.sock.write(b"\xe0\0")
        except Exception:
            pass
        try:
            self.sock.close()
        except Exception:
            pass
        self.sock = None

    def ping(self):
        self.sock.write(b"\xc0\0")

    def publish(self, topic, msg, retain=False, qos=0):
        if isinstance(topic, str):
            topic = topic.encode()
        if isinstance(msg, str):
            msg = msg.encode()

        pkt = bytearray(b"\x30\0\0\0")
        pkt[0] |= (qos << 1) | (1 if retain else 0)

        sz = 2 + len(topic) + len(msg)
        if qos > 0:
            sz += 2

        assert sz < 2097152
        i = 1
        x = sz
        while x > 0x7f:
            pkt[i] = (x & 0x7f) | 0x80
            x >>= 7
            i += 1
        pkt[i] = x

        self.sock.write(pkt[:i + 1])
        self._send_str(topic)

        if qos > 0:
            self.pid += 1
            pid = self.pid
            struct.pack_into("!H", pkt, 0, pid)
            self.sock.write(pkt[:2])

        self.sock.write(msg)

        # For MVP: we keep qos=0 (no ACK wait). QoS1 support omitted for simplicity.


# ============================================================
# UART I/O
# ============================================================

def init_uart():
    if machine is None:
        raise RuntimeError("machine module not available; can't open UART on this firmware")

    uart = machine.UART(UART_PORT, baudrate=UART_BAUD)
    return uart

def uart_read_nonblocking(uart, max_bytes=256):
    try:
        n = uart.any()
        if not n:
            return b""
        n = min(n, max_bytes)
        return uart.read(n) or b""
    except Exception:
        # Fallback if .any() not supported
        try:
            return uart.read(max_bytes) or b""
        except Exception:
            return b""


# ============================================================
# PACKET PARSER
# ============================================================

def extract_frames_from_rxbuf(rx_buf):
    """
    Consume rx_buf and return (frames, new_rx_buf)
    frames is a list of dicts: {"ts_ms", "id", "len", "data_hex"}
    """
    frames = []

    while True:
        # Find START_BYTE
        start_idx = rx_buf.find(bytes([START_BYTE]))
        if start_idx < 0:
            # Keep a small tail in case START spans boundary
            if len(rx_buf) > PKT_LEN:
                rx_buf = rx_buf[-(PKT_LEN - 1):]
            return frames, rx_buf

        # Not enough bytes for full packet
        if len(rx_buf) < start_idx + PKT_LEN:
            # Drop junk before start to keep buffer small
            if start_idx > 0:
                rx_buf = rx_buf[start_idx:]
            return frames, rx_buf

        candidate = rx_buf[start_idx:start_idx + PKT_LEN]

        # Validate END byte
        if candidate[16] != END_BYTE:
            # Drop this start and resync
            rx_buf = rx_buf[start_idx + 1:]
            continue

        # Parse fields
        can_id = le_u16(candidate[1], candidate[2])
        length = candidate[3]
        if length > 8:
            length = 8
        data8 = candidate[4:12]  # always 8 bytes in the packet
        ts = le_u32(candidate[12], candidate[13], candidate[14], candidate[15])

        frames.append({
            "ts_ms": ts,
            "id": can_id,
            "len": length,
            "data_hex": hex8(data8)
        })

        # Consume through this packet
        rx_buf = rx_buf[start_idx + PKT_LEN:]


# ============================================================
# MQTT CONNECTION / PUBLISH LOOP
# ============================================================

def test_at_health():
    # Optional: prints a quick health snapshot
    try:
        ai = xbee.atcmd("AI")
        db = xbee.atcmd("DB")
        vplus = xbee.atcmd("V+")
        print("[AT] AI=0x{:02X} DB=-{}dBm V+={}mV".format(ai, db, vplus))
    except Exception as e:
        print("[AT] health read failed:", e)

def connect_mqtt():
    client = MQTTClient(
        CLIENT_ID,
        AWS_ENDPOINT,
        port=MQTT_PORT,
        ssl=True,
        ssl_params=SSL_PARAMS,
        keepalive=60
    )
    client.connect()
    return client

def build_batch_payload(frames):
    # JSON payload, versioned.
    # You can change this later without changing the STM32.
    payload = {
        "v": 1,
        "frames": frames
    }
    return ujson.dumps(payload)

def maybe_reset_module(consecutive_failures):
    if consecutive_failures >= FAIL_RESET_THRESHOLD:
        print("[SYSTEM] too many failures; resetting module")
        # On some Digi firmwares this exists:
        try:
            xbee.reset()
        except Exception:
            # fallback: long sleep (a human may power cycle)
            try:
                xbee.sleep_now(10000)
            except Exception:
                sleep_ms(10000)

def main():
    print("[BOOT] XBee UART->AWS IoT bridge starting")
    test_at_health()

    uart = init_uart()

    mqtt = None
    mqtt_connected = False

    rx_buf = bytearray()
    batch = []
    last_flush = now_ms()

    # stats
    frames_parsed = 0
    frames_published = 0
    publish_errors = 0
    parse_resyncs = 0

    consecutive_failures = 0
    retry_ms = RETRY_MIN_MS

    last_health_print = now_ms()

    while True:
        try:
            # ---- Ensure MQTT connection ----
            if not mqtt_connected or mqtt is None:
                try:
                    mqtt = connect_mqtt()
                    mqtt_connected = True
                    consecutive_failures = 0
                    retry_ms = RETRY_MIN_MS
                    print("[MQTT] connected")
                except Exception as e:
                    mqtt_connected = False
                    consecutive_failures += 1
                    print("[MQTT] connect failed ({}): {}".format(consecutive_failures, e))
                    maybe_reset_module(consecutive_failures)
                    sleep_ms(retry_ms)
                    retry_ms = min(retry_ms * 2, RETRY_MAX_MS)
                    continue  # try again

            # ---- Read UART data ----
            chunk = uart_read_nonblocking(uart, max_bytes=256)
            if chunk:
                rx_buf.extend(chunk)
                if len(rx_buf) > MAX_RX_BUF:
                    # If we are falling behind, drop oldest bytes to recover.
                    rx_buf = rx_buf[-MAX_RX_BUF:]

                frames, rx_buf = extract_frames_from_rxbuf(rx_buf)
                if frames:
                    batch.extend(frames)
                    frames_parsed += len(frames)

            # ---- Flush batch if needed ----
            t = now_ms()
            if batch:
                if (len(batch) >= BATCH_MAX_FRAMES) or (elapsed_ms(last_flush) >= BATCH_FLUSH_MS):
                    payload = build_batch_payload(batch)
                    try:
                        mqtt.publish(TOPIC_PUB, payload, qos=0)
                        frames_published += len(batch)
                        batch.clear()
                        last_flush = t
                    except Exception as e:
                        publish_errors += 1
                        print("[MQTT] publish failed:", e)
                        mqtt_connected = False
                        consecutive_failures += 1
                        maybe_reset_module(consecutive_failures)
                        try:
                            mqtt.disconnect()
                        except Exception:
                            pass
                        mqtt = None
                        # Keep batch, but cap growth
                        if len(batch) > MAX_BATCH_FRAMES_HARD_CAP:
                            batch = batch[-MAX_BATCH_FRAMES_HARD_CAP:]

            # ---- Health print occasionally ----
            if elapsed_ms(last_health_print) >= 5000:
                last_health_print = now_ms()
                try:
                    ai = xbee.atcmd("AI")
                    db = xbee.atcmd("DB")
                    print("[HEALTH] AI=0x{:02X} DB=-{}dBm parsed={} published={} pubErr={} batch={}".format(
                        ai, db, frames_parsed, frames_published, publish_errors, len(batch)
                    ))
                except Exception:
                    print("[HEALTH] parsed={} published={} pubErr={} batch={}".format(
                        frames_parsed, frames_published, publish_errors, len(batch)
                    ))

            # Small sleep so we don’t spin at 100% CPU
            sleep_ms(5)

        except Exception as e:
            # Catch-all: never die. Reset MQTT and keep going.
            print("[LOOP] exception:", e)
            mqtt_connected = False
            consecutive_failures += 1
            maybe_reset_module(consecutive_failures)
            try:
                if mqtt:
                    mqtt.disconnect()
            except Exception:
                pass
            mqtt = None
            sleep_ms(200)


if __name__ == "__main__":
    main()