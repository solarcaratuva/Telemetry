from umqtt.simple import MQTTClient
import network
import time
import ujson  # We use this to make perfect JSON automatically

# --- Static AWS Parameters ---
# Keep your specific endpoint here
HOST = b'a14ezejktp3brt-ats' 
CLIENT_ID = "car1_lte_module"

# SSL certificates
SSL_PARAMS = {'keyfile': "/flash/cert/aws.key",
              'certfile': "/flash/cert/aws.crt",
              'ca_certs': "/flash/cert/aws.ca"}

# CRITICAL: This topic matches your IoT Rule (4 segments)
TOPIC = "solarcar/us-east-1/car1/telemetry"

def publish_telemetry(payload_dict, region, client_id=CLIENT_ID, host_prefix=HOST, sslp=SSL_PARAMS):
    
    # Handle Region
    if isinstance(region, str):
        region = region.encode('utf-8')
    hostname = b'%s.iot.%s.amazonaws.com' % (host_prefix, region)

    # Convert the dictionary to a JSON string
    # This automatically handles quotes and formatting
    message_json = ujson.dumps(payload_dict)

    print("- Connecting to %s..." % hostname)
    try:
        client = MQTTClient(client_id, hostname, ssl=True, ssl_params=sslp)
        client.connect()
        print("[CONNECTED]")
        
        print("- Publishing to %s..." % TOPIC)
        print("- Payload: %s" % message_json)
        client.publish(TOPIC, message_json)
        print("[SENT]")
        
        client.disconnect()
        print("- Disconnected")
    except Exception as e:
        print("[ERROR] Publish failed: %s" % e)

# --- Main Execution ---

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