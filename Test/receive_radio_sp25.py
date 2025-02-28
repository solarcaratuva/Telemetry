import serial
import time

SERIAL_PORT = "COM5"  # Set this to your ST-Link COM port
BAUD_RATE = 115200    # Match the USB Serial baud rate (115200)

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Listening for forwarded XBee messages on {SERIAL_PORT}...")

    while True:
        line = ser.readline().decode('utf-8', errors='replace').strip()
        if line:
            print("Received from ST-Link:", line)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")

except Exception as e:
    print("Error:", e)

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
