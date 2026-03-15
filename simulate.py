import sys
import struct
import time
import threading

# --------------------------------------------------------------------
# 1. Mock the hardware modules that main.py expects
# --------------------------------------------------------------------

class MockUART:
    def __init__(self, port, baudrate):
        self.port = port
        self.baudrate = baudrate
        self._buffer = bytearray()
        self._lock = threading.Lock()

    def any(self):
        with self._lock:
            return len(self._buffer)

    def read(self, n):
        with self._lock:
            data = self._buffer[:n]
            self._buffer = self._buffer[n:]
            return bytes(data)

    def inject_data(self, data: bytes):
        """Helper to simulate receiving data from STM32"""
        with self._lock:
            self._buffer.extend(data)


class MockMachine:
    def __init__(self):
        self.UART = MockUART

class MockXBee:
    def atcmd(self, cmd):
        # Fake health metrics
        if cmd == "AI": return 0x00
        if cmd == "DB": return 55
        if cmd == "V+": return 3300
        return 0

    def wrap_socket(self, sock, **kwargs):
        raise NotImplementedError("MQTT socket not mocked for local test")

# Inject them into sys.modules so 'import machine', 'import xbee', etc. work
sys.modules['machine'] = MockMachine()
sys.modules['xbee'] = MockXBee()
sys.modules['usocket'] = __import__('socket')
sys.modules['ustruct'] = __import__('struct')
sys.modules['ujson'] = __import__('json')


# --------------------------------------------------------------------
# 2. Import the main script
# --------------------------------------------------------------------
try:
    import main
except ImportError as e:
    print(f"Failed to import main.py: {e}")
    sys.exit(1)


# --------------------------------------------------------------------
# 3. Create a fake STM32 data generator
# --------------------------------------------------------------------
def stm32_simulator(uart_instance):
    """Runs in a background thread, stuffing fake CAN frames into the UART."""
    print("[SIMULATOR] Starting fake STM32 data stream...")
    frame_count = 0
    
    while True:
        # Build a valid 17-byte frame according to main.py specs:
        # START(1) + ID(2) + LEN(1) + DATA(8) + TS(4) + END(1)
        
        start_byte = 0xA5
        end_byte   = 0x5A
        
        can_id = 0x123 + (frame_count % 10)  # Vary the ID slightly
        length = 8
        
        # Fake 8-byte payload: e.g. [01, 02, 03, 04, 05, 06, 07, 08]
        data = bytes([1, 2, 3, 4, 5, 6, 7, frame_count % 256])
        
        # Timestamp in ms
        ts_ms = int(time.time() * 1000) & 0xFFFFFFFF
        
        # Pack everything (little-endian for ID and TS as expected by main.py)
        # B: uint8, <: little-endian, H: uint16, 8s: 8 bytes string, I: uint32
        packet = struct.pack("<BBH B 8s I B", 
                             start_byte,    # We pack START twice here? No, struct format:
                             # Let's pack manually to be safe, since main.py is very specific about layout
                             0, 0, 0, b'', 0, 0) # dummy
                             
        # Manual packing to perfectly match extraction indices:
        # candidate[0] = START
        # candidate[1:3] = ID
        # candidate[3] = LEN
        # candidate[4:12] = DATA
        # candidate[12:16] = TS
        # candidate[16] = END
        packet = bytearray(17)
        packet[0] = 0xA5
        packet[1] = can_id & 0xFF
        packet[2] = (can_id >> 8) & 0xFF
        packet[3] = 8
        packet[4:12] = data
        packet[12] = ts_ms & 0xFF
        packet[13] = (ts_ms >> 8) & 0xFF
        packet[14] = (ts_ms >> 16) & 0xFF
        packet[15] = (ts_ms >> 24) & 0xFF
        packet[16] = 0x5A
        
        # Inject into the mocked UART buffer
        uart_instance.inject_data(packet)
        frame_count += 1
        
        time.sleep(0.05)  # Send ~20 frames per second


# --------------------------------------------------------------------
# 4. Run the simulation
# --------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("WARNING: This simulation only works if DEBUG_TO_FILE = True")
    print("         in main.py. Press Ctrl+C to stop.")
    print("=" * 60)
    
    # We must patch init_uart in main.py to return our mocked UART
    # before we call main.main()
    original_init = main.init_uart
    
    mock_uart_instance = MockUART(1, 115200)
    
    def fake_init_uart():
        return mock_uart_instance
        
    main.init_uart = fake_init_uart
    
    # Start the background thread generating data
    t = threading.Thread(target=stm32_simulator, args=(mock_uart_instance,), daemon=True)
    t.start()
    
    # Run the main loop (this blocks forever until Ctrl+C)
    try:
        main.main()
    except KeyboardInterrupt:
        print("\n[SIMULATOR] Stopped by user. Check debug_log.txt for output!")
