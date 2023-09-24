import serial

# Define the serial port and baud rate for the XBee module
serial_port = '/dev/ttyUSB1'  # Change this to the correct port on your system
baud_rate = 9600

# Create a serial connection to the XBee module
try:
    xbee_serial = serial.Serial(serial_port, baud_rate)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

# Function to continuously read and print data
def receive_data():
    try:
        while True:
            data = xbee_serial.readline().decode().strip()
            if data:
                print(f"Received: {data}")
    except KeyboardInterrupt:
        pass

# Main execution
if __name__ == "__main__":
    print("Listening for incoming data...")
    receive_data()

# Close the serial connection when the script is interrupted
xbee_serial.close()
print("Serial port closed.")