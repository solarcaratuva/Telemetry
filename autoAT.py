# Copyright (c) 2019, Digi International, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from umqtt.simple import MQTTClient
import network
import time
import xbee

# --- Static AWS Parameters ---
HOST = b'a14ezejktp3brt-ats'
CLIENT_ID = "clientID"

# REGION = b'FILL_ME_IN'   ex: b'us-east-1'

# SSL certificates.
SSL_PARAMS = {'keyfile': "/flash/cert/aws.key",
              'certfile': "/flash/cert/aws.crt",
              'ca_certs': "/flash/cert/aws.ca"}

TOPIC = "test/xbee"

# --- Function modified to take parameters ---

def publish_test(message, region, client_id=CLIENT_ID, host_prefix=HOST, sslp=SSL_PARAMS):

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
    message_json = '{"message": "%s"}' % message
    client.publish(TOPIC, message_json)
    print("[OK]")
    
    # Disconnect.
    client.disconnect()
    print("- Done")


def sub_cb(topic, msg):
    """
    Callback executed when messages from subscriptions are received. Prints
    the topic and the message.

    :param topic: Topic of the message.
    :param msg: Received message.
    """

    global msgs_received

    msgs_received += 1
    print("- Message received!")
    print("   * %s: %s" % (topic.decode("utf-8"), msg.decode("utf-8")))


def subscribe_test(region, client_id=CLIENT_ID, sslp=SSL_PARAMS,
                   msg_limit=2):
    """
    Connects to AWS, subscribes to a topic and starts listening for messages.

    :param region: region specified for hostname
    :param client_id: Unique identifier for the device connected.
    :param hostname: AWS hostname to connect to.
    :param sslp: SSL certificate parameters.
    :param msg_limit: Maximum number of messages to receive before
        disconnecting from AWS..
    """

    global msgs_received

    hostname = b'%s.iot.%s.amazonaws.com' % (HOST, region)

    # Connect to AWS.
    client = MQTTClient(client_id, hostname, ssl=True, ssl_params=sslp)
    client.set_callback(sub_cb)
    print("- Connecting to AWS... ", end="")
    client.connect()
    print("[OK]")
    # Subscribe to topic.
    print("- Subscribing to topic '%s'... " % TOPIC, end="")
    client.subscribe(TOPIC)
    print("[OK]")
    # Wait for messages.
    msgs_received = 0
    print('- Waiting for messages...')
    while msgs_received < msg_limit:
        client.check_msg()
        time.sleep(1)
    # Disconnect.
    client.disconnect()
    print("- Done")



print(" +--------------------------------------+")
print(" | XBee MicroPython AWS Publish Message |")
print(" +--------------------------------------+\n")

conn = network.Cellular()

print("- Waiting for the module to be connected to the cellular network... ",
      end="")
while not conn.isconnected():
    time.sleep(5)
print("[OK]")
print()

xb = xbee.XBee()

while conn.isconnected():
    print("ATAI Output: " + xb.atcmd('AI'))
    print("ATDB Output: " + network.Cellular().signal())
    time.sleep(30)

print("Program stopped: LTE disconnected from cellular network.")