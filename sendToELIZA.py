"""Digi XBee LTE ELIZA TCP client.

Sends "Hello World!" every five seconds and appends server responses to the
module file system.
"""

import socket

from umqtt.simple import MQTTClient
import network
import time


SERVER_ADDRESS = "52.43.121.77"
SERVER_PORT = 0x2328  # 9000
MESSAGE = b"Hello World!"
LOG_FILE = "ELIZAlog.txt"
PERIOD_SECONDS = 5
RECEIVE_TIMEOUT_SECONDS = 2


def log_response(data):
	"""Append a timestamped server response to the log file."""
	if not data:
		return

	try:
		response = data.decode("utf-8")
	except Exception:
		response = repr(data)

	with open(LOG_FILE, "a") as log:
		log.write("{}: {}\n".format(time.time(), response))


def main():
	while True:
		sock = None
		try:
			# A new connection is used for each message so the script can
			# recover cleanly if the cellular connection is interrupted.
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.settimeout(RECEIVE_TIMEOUT_SECONDS)
			sock.connect((SERVER_ADDRESS, SERVER_PORT))
			sock.send(MESSAGE)

			while True:
				try:
					response = sock.recv(1024)
					if not response:
						break
					log_response(response)
				except socket.timeout:
					break
		except Exception as error:
			with open(LOG_FILE, "a") as log:
				log.write("{}: ERROR: {}\n".format(time.time(), error))
		finally:
			if sock is not None:
				try:
					sock.close()
				except Exception:
					pass

		time.sleep(PERIOD_SECONDS)


# main()

print(" +--------------------------------------+")
print(" |   Solar Car Telemetry Transmitter    |")
print(" +--------------------------------------+\n")

conn = network.Cellular()
print("- Connecting to Cellular... ", end="")
while not conn.isconnected():
    time.sleep(5)
print("[OK]")

# Optional: Sync time with network so 'ts' is accurate
# (Most Cellular modules do this automatically, but good to be aware)
print("- Current System Time: {%s}" % time.time()) 

while True:
    # 1. Get User Input
    user_message = input("\nEnter message to send (or 'q' to quit): ")
    
    if user_message.lower() == 'q':
        break
        
    # 2. Build the Dictionary
    # We create the structure here. 'ts' is generated automatically.
    packet = {
        "ts": int(time.time()),  # Current Unix Timestamp
        "message": user_message
    }
    
    # 3. Send it
    # We pass 'us-east-1' because that is where your database lives
    publish_telemetry(packet, region="us-east-1")