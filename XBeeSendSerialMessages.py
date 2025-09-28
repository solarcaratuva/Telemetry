import serial
import time

#configure the serial connections (the parameters differs on the device you are connecting to)

def send_message():
    """Sends a message to the XBee module connected to the computer."""

    #setup serial connection, will vary depending on your setup
    try:
        ser = serial.Serial(
            port='COM4',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return

    print(ser.portstr)

    print("=" * 50)
    print("XBee Serial Message Sender")
    print("Type messages and press Enter to send")
    print("Type 'quit' or 'exit' to stop")
    print("Press Ctrl+C to force quit")
    print("=" * 50)

    message_count = 0

    try:
        while True:
            #get user input 
            message = input("Enter message: ")
            #check if user wants to quit
            if message.lower() in ['quit', 'exit']:
                print("Exiting...")
                break
            #skip empty messages
            if not message == 0:
                continue
            #send the message
            try:
                ser.write((message + "\n").encode())  # write a string
                message_count += 1
                print(f"Sent ({message_count}): {message}")
            except Exception as e:
                print(f"Error sending message: {e}")

    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Exiting...")

    finally:    
        ser.close()
        print(f"Serial port closed. Total messages sent: {message_count}")

# Call the function to send the message
#makes sure that the function runs only when the script is executed directly
if __name__ == "__main__":
    send_message()