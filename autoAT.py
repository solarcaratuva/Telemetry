from umqtt.simple import MQTTClient
import network
import time
import xbee
from machine import Pin

# --- Static AWS Parameters ---
HOST = b'a14ezejktp3brt-ats'
CLIENT_ID = "clientID"

REGION = b'us-east-1' # if not the region in AWS, switch it using enterRegion()

# SSL certificates.
SSL_PARAMS = {'keyfile': "/flash/cert/aws.key",
              'certfile': "/flash/cert/aws.crt",
              'ca_certs': "/flash/cert/aws.ca"}

TOPIC = "solarcar/us-east-1/car1/telemetry"


# Use if region is not 'us-east-1'
def enterRegion(newRegion):
    REGION = newRegion


print(" +--------------------------------------+")
print(" | XBee MicroPython AWS Publish Message |")
print(" +--------------------------------------+\n")

xb = xbee.XBee()

conn = network.Cellular()

print("- Waiting for the module to be connected to the cellular network... ",
      end="")
while not conn.isconnected():
    print()
    print("ATAI Output: %s" % xb.atcmd('AI'))
    print("ATDB Output: %s" % network.Cellular().signal())
    time.sleep(10)
print("[OK]")
print()


button = Pin.board.D4
button.mode(Pin.IN)

count = 0
while conn.isconnected():
    count += 1
    if (count == 10):
        print("ATAI Output: %s" % xb.atcmd('AI'))
        print("ATDB Output: %s" % network.Cellular().signal())
        count = 0
    if (button.value() == 0):
        print("User button pressed")
        break
    time.sleep(1)

print("Program stopped: LTE disconnected from cellular network.")


