print("--- Running aws_test.py (Corrected Version) ---")

# 1. Import the library from /lib/umqtt/simple.py
from lib.umqtt.simple import MQTTClient

# 2. Import other needed tools
import time
import network
import json

# --- 3. AWS CONFIGURATION - YOU MUST EDIT THIS! ---

# Get this from AWS IoT -> Settings -> Endpoint
AWS_ENDPOINT = "a14ezejktp3brt-ats.iot.us-east-2.amazonaws.com"

# This must be a unique name for this device
CLIENT_ID = "XBEEMODULE"

# This is the "channel" you will send messages to
MQTT_TOPIC = "test/xbee"

# --- 4. CERTIFICATE FILE PATHS ---
# This dictionary is passed directly to the MQTT client.
# These paths MUST match the files in your /flash/certs/ directory.
SSL_PARAMS = {
    "keyfile": "/flash/cert/aws.key",
    "certfile": "/flash/cert/aws.crt",
    "ca_certs": "/flash/cert/aws.ca"
}

# --- 5. Main script logic ---

print("Waiting for cellular network...")
# A simple sleep is OK for testing.
# A real script should use network.wait_for_conn().
time.sleep(10)
print("Network should be ready.")

# Create the MQTT client
# This time, we pass the ssl_params dictionary directly.
print("Creating MQTT client...")
try:
    mqtt = MQTTClient(
        client_id=CLIENT_ID,
        server=AWS_ENDPOINT,
        port=8883,       # Port 8883 is standard for MQTT over SSL
        ssl=True,
        ssl_params=SSL_PARAMS
    )
except Exception as e:
    print(f"Error creating MQTTClient: {e}")
    # Stop the script if this failed
    raise

# Try to connect and publish
try:
    print(f"Connecting to AWS IoT at {AWS_ENDPOINT}...")
    mqtt.connect()
    print("Successfully connected to AWS IoT!")

    # --- THIS IS WHERE THE MESSAGE IS SENT ---
    message_payload = json.dumps({
        "message": "Hello from XBee!",
        "timestamp": time.time()
    })
    
    print(f"Publishing to topic '{MQTT_TOPIC}': {message_payload}")
    mqtt.publish(MQTT_TOPIC, message_payload)
    print("Message published successfully.")

    mqtt.disconnect()
    print("Disconnected. Script finished.")

except Exception as e:
    print(f"ERROR: Failed to connect or publish: {e}")
    print("Please check your AWS Endpoint, certificate paths, and network connection.")

print("--- End of aws_test.py ---")