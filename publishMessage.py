from umqtt.simple import MQTTClient
import network
import time

# --- Static AWS Parameters ---
HOST = b'a14ezejktp3brt-ats'
CLIENT_ID = "clientID"

# SSL certificates.
SSL_PARAMS = {'keyfile': "/flash/cert/aws.key",
              'certfile': "/flash/cert/aws.crt",
              'ca_certs': "/flash/cert/aws.ca"}

TOPIC = "solarcar/us-east-1/car1/telemetry"
REGION = "us-east-1"

# Use if region is not 'us-east-1'
def enterRegion(newRegion):
    REGION = newRegion
    print("Current region: " + newRegion)

# Publishing message method
def publish_test(message, region=REGION, client_id=CLIENT_ID, host_prefix=HOST, sslp=SSL_PARAMS):

    # Build the AWS endpoint dynamically using the region parameter
    # This ensures it works even if you pass a normal string
    if isinstance(region, str):
        region = region.encode('utf-8')
    
    hostname = b'%s.iot.%s.amazonaws.com' % (host_prefix, region)

    # Connect to AWS.
    client = MQTTClient(client_id, hostname, ssl=True, ssl_params=sslp)
    print("- Connecting to AWS... ", end="")
    client.connect()
    print("[OK]")
    
    # Publish the parameterized message.
    print("- Publishing message... ", end="")
    message_json = '{"message": "%s", "ts": %s}' % message, time.time(), # for timestamp
    client.publish(TOPIC, message_json)
    print("[OK]")
    
    # Disconnect.
    client.disconnect()
    print("- Done")


print(" +--------------------------------------+")
print(" | XBee MicroPython AWS Publish Message |")
print(" +--------------------------------------+\n")

print("MQTT Topic: %s" % TOPIC)
print("Current region: %s" % REGION)

conn = network.Cellular()

print("- Waiting for the module to be connected to the cellular network... ",
      end="")
while not conn.isconnected():
    time.sleep(5)
print("[OK]")