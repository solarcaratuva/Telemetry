# Telemetry XBee to AWS IoT Bridge

(describes main.py and simulate.py)

This project contains a MicroPython script (`main.py`) designed to run on a Digi XBee LTE module. It bridges telemetry CAN messages sent via UART from an STM32 microcontroller to AWS IoT Core over MQTT.

## File Structure: `main.py`

The script is divided into several logical sections:

### 1. Configuration (`CONFIG`)
Defines essential parameters for the application:
- **AWS & MQTT**: Endpoint, Client ID, topic, and certificates for TLS.
- **UART settings**: Baud rate and port for receiving CAN frames from the STM32 board.
- **Packet Structure**: Start byte (`0xA5`), end byte (`0x5A`), and total packet length (17 bytes) tailored to the STM32 CAN payload.
- **Batching & Retry logic**: Controls how many messages are queued before sending an MQTT publish (to save bandwidth and power) and defines failure thresholds that trigger module resets.

### 2. Utilities (`SMALL UTILS`)
Standard lightweight helper functions for:
- Timing (`now_ms`, `elapsed_ms`, `sleep_ms`).
- Converting little-endian byte sequences to integers (`le_u16`, `le_u32`).
- Formatting binary data into hex strings (`hex8`).

### 3. MQTT Client (`MQTT CLIENT`)
A custom, minimal MQTT client implemented specifically for MicroPython:
- Leverages XBee's secure socket wrapper (`xbee.wrap_socket`) for TLS communication.
- Handles connect, publish, ping, and disconnect logic via raw byte construction (minimizing memory footprint).

### 4. UART I/O
Provides straightforward, non-blocking serial read functionality to fetch chunks of incoming bytes from the hardware UART buffer without stalling the main loop.

### 5. Packet Parser (`PACKET PARSER`)
The core decoding logic (`extract_frames_from_rxbuf`):
- Scans the raw incoming byte stream for the `0xA5` start and `0x5A` end bytes.
- Extracts the message timestamp, CAN ID, payload length, and 8 bytes of data.
- Drops malformed packets or trims invalid bytes, returning structured dictionaries of verified frames.

### 6. Main Loop (`MQTT CONNECTION / PUBLISH LOOP`)
The entry point `main()` orchestrates the entire application flow:
- Initializes the UART interface.
- Continually reads incoming bytes and feeds them to the packet parser.
- Collects decoded messages into a batch.
- Automatically connects and reconnects to AWS IoT when disconnected.
- Periodically flushes batched messages as JSON payloads over MQTT.
- Logs board health metrics (cellular signal/DB, parsed frames, errors) and triggers an automated software reset if repeated failures occur.


---

## Simulating the Script Locally (`simulate.py`)

If you want to run testing locally on a Windows/Mac/Linux machine without deploying to physical Digi XBee hardware, you can use the Included `simulate.py` runner script.

### Requirements
You must have `DEBUG_TO_FILE = True` set in `main.py` before running the simulation, as the local python environment does not support actual outbound AWS/XBee socket wrapping.

### Running the Simulator
Run this from your terminal:
```bash
python simulate.py
```
Press `Ctrl+C` to stop the script, and check `debug_log.txt` to see the artificially generated UART captures.

### How `simulate.py` Works

The simulation script uses several tricks to mimic the physical hardware environment:
1. **Mocking Hardware Modules**: `main.py` relies on `import machine` and `import xbee`, which do not exist outside of MicroPython. The simulator injects mock classes directly into `sys.modules`, bypassing those import errors and intercepting calls to methods like `xbee.atcmd("DB")` to return fake health metrics (e.g. -55dBm).
2. **Mocking the UART Interface**: It replaces the physical hardware RX serial line with a custom thread-safe bytearray (`MockUART`).
3. **Fake STM32 Threads**: An active background thread spawns loops that continually synthesize perfectly-formatted 17-byte CAN frames (with the required `0xA5` sync bytes and little-endian sizes) and injects them directly into the MockUART buffer.
4. **Execution Hijacking**: The script patches `main.init_uart()` directly in memory so that when `main.main()` is called, the core loop reads from the testing buffer instead of an actual serial physical port.

### Understanding the `debug_log.txt` Output
When running the script with `DEBUG_TO_FILE = True`, you'll see lines generated in the `debug_log.txt` file formatted like this:
```text
TS: 4075590601, ID: 0x123, LEN: 8, DATA: 010203040506070A
```
This represents a decoded CAN frame sent from the STM32. Here is what each field means:
*   **TS (Timestamp)**: The timestamp (in milliseconds) at which the STM32 recorded the message, read as a 32-bit unsigned little-endian integer.
*   **ID (CAN ID)**: The hexadecimal identifier of the CAN bus message, indicating what specific sensor, component, or unit the data is coming from (read as a 16-bit little-endian integer). 
*   **LEN (Data Length)**: The number of valid bytes in the data payload (usually exactly 8 bytes for standard CAN 2.0 frames).
*   **DATA**: The raw payload bytes expressed as a concatenated hex string. This contains the actual telemetry values (e.g., motor RPM, battery voltage) that correspond to the given `ID`.
