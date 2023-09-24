import serial
import time

# Define the serial port and baud rate for the XBee module
serial_port = '/dev/ttyUSB0'  # Change this to the correct port on your system
baud_rate = 9600

# Create a serial connection to the XBee module
try:
    xbee_serial = serial.Serial(serial_port, baud_rate)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# Function to send a signal
def send_signal():
    message = "Hello, XBee!"  # Message to send
    xbee_serial.write(message.encode())  # Send the message
    print(f"Sent: {message}")

# Main loop
try:
    while True:
        send_signal()
        time.sleep(.25)  # Send a signal every 5 seconds
except KeyboardInterrupt:
    # Close the serial connection when the script is interrupted
    xbee_serial.close()
    print("Serial port closed.")