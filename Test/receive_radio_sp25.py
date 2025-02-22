import serial
import time

# Change the port name as needed. For Windows, it might be "COM3", for Linux, "/dev/ttyUSB0" or similar.
SERIAL_PORT = "COM3"  
BAUD_RATE = 9600

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print("Listening for XBee messages on", SERIAL_PORT, "at", BAUD_RATE, "baud...")
    
    while True:
        line = ser.readline().decode('utf-8', errors='replace').strip()
        if line:
            print("Received:", line)
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")

except Exception as e:
    print("Error:", e)

finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
