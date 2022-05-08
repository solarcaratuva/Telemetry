from base64 import encode
import time
import serial
from digi.xbee.devices import XBeeDevice
import json
import CANmessages.can_bp as can_bp

import sqlite3

import random


id_to_message = {
    # '0b10110': 'Cell Voltage',
    # '0b1110': 'PackInformation',
    # '0b100101': 'Solar Voltage'
    '0x106': 'BPSError',
    '0x115': 'MotorControllerError',
    '0x123': 'PowerAuxError',
    '0x201': 'ECUMotorCommands',
    '0x301': 'ECUPowerAuxCommands',
    '0x315': 'MotorControllerDriveStatus',
    '0x325': 'MotorControllerPowerStatus',
    '0x406': 'BPSPackInformation',
    '0x416': 'BPSCellVoltage',
    '0x426': 'BPSCellTemperature',
    '0x434': 'SolarCurrent',
    '0x444': 'SolarVoltage',
    '0x454': 'SolarTemp',
    '0x464': 'SolarPhoto'
}

PORT = "/dev/tty.usbserial-0001"
BAUD_RATE = 9600
class xbeeReceiver(object):
    def __init__(self):
        self.xbee = XBeeDevice(PORT, BAUD_RATE)
        self.xbee.open()
        # self.xbee = serial.Serial(PORT, BAUD_RATE)

    def read_data(self):
        return self.xbee.read_data()
        # ret = ""
        # while self.xbee.in_waiting:
        #     byt = self.xbee.read(1).decode()
        #     ret += byt
        # return ret


    def receiveMessage(self):
        encoded_json = self.xbee.read_data()

        if encoded_json is not None:
            decoded = encoded_json.data.decode()
            print(decoded)
            jaunt = json.loads(decoded)

            toret = {}
            for message in jaunt:
                # print()
                # print(message)
                # print()
                # print(self.formatMessage(message))
                # toret.append(self.formatMessage(message))
                newinfo = self.formatMessage(message)

                # this merges them into a single dictionary
                toret = {**toret, **newinfo}

            print(toret)
            return toret
            # decoded = encoded_json.data.decode()
            # print(decoded)
            # jaunt = json.loads(decoded)
            
            # message_id = jaunt['message_id']
            # message = jaunt['message']

            # to_decode_bytes = bytes.fromhex(message[2:])
        

            # PackInfo = bps.PackInformation()

            # PackInfo.decode(to_decode_bytes)

            # toret = json.loads(PackInfo.to_json())


            # return toret

        return None

    def formatMessage(self, one_message):
        message_id = one_message['id']
        message = one_message['data']
        error = one_message['err']
        message_id_decoded = id_to_message[message_id]

        to_decode_bytes = bytes.fromhex(message[2:])

        can_type = None
        if message_id_decoded == 'Cell Voltage':
            can_type = can_bp.CellVoltage()
        elif message_id_decoded == "PackInformation":
            can_type = can_bp.PackInformation()
        elif message_id_decoded == "Solar Voltage":
            can_type = can_bp.SolarVoltage()

        # print(message_id_decoded)
        # print(message)
        to_decode_bytes = bytes.fromhex(message[2:])
        can_type.decode(to_decode_bytes)

        return json.loads(can_type.to_json())




        #return decodeJSON(encoded_json)

receiver = xbeeReceiver()


conn = sqlite3.connect('../app.db')

cur = conn.cursor()


sql = 'SELECT MAX(ID) FROM "TestData"'

try: 
    cur.execute(sql)
    start_id = cur.fetchone()[0] + 1
    
except:
    start_id = 0


sql = 'SELECT MAX(RUN_ID) FROM "TestData"'
try:
    cur.execute(sql)
    start_run_id = cur.fetchone()[0] + 1
except:
    start_run_id = 18


print("Run ID:", start_run_id)

increment = 0
while True:
    data = receiver.receiveMessage()
    if data is not None:
        print(data)

        # for item in temp:
        #     temp['message_id'] = id_to_message[temp['message_id']]

        # print(temp)


        
        

        db_obj = {
            'id': start_id + increment,
            'timestamp': time.time(),
            # 'run_id': 18,
            'run_id': start_run_id,
            'mph': 18+2*increment,
            'rpm': 18-increment,
            'miles': 18+increment,
            'soc': random.randint(1,100),
            'min_voltage': data['pack_voltage'],
            'max_voltage': data['pack_voltage'],
            'voltage': data['pack_voltage'],
            'min_current': data['pack_current'],
            'max_current': data['pack_current'],
            'current': data['pack_current'],
            'min_temperature': 18,
            'max_temperature': 18,
            'temperature': 18,
            'json': data
        }
        for key in db_obj:
            print(key)

        row = [str(db_obj[key]) for key in db_obj]
        # row.pop()
        row[-1] = "NULL"

        arr_string = ','.join(row)
        print(arr_string)
        sql = 'INSERT INTO "TestData" VALUES({});'.format(arr_string) 
        cur.execute(sql)       
        conn.commit()

        increment+=1
        # db_obj


    print("Yo")

    time.sleep(1)


# while True:
#     temp = receiver.receiveMessage()
#     if temp is not None:
#         # print(temp)
#         # print(temp.data)
#         print(temp.data.decode())
#         decoded = temp.data.decode()
#         jaunt = (json.loads(decoded))

#         message_id = jaunt['message_id']
#         message = jaunt['message']

#         #message is a string of hex with 0x right now

#         print(message[2:])

#         # message = "0a000b0064080200"

#         to_decode_bytes = bytes.fromhex(message[2:])
        

#         PackInfo = bps.PackInformation()

#         print(to_decode_bytes)
#         PackInfo.decode(to_decode_bytes)

#         print(PackInfo.to_json())


#     print("Yo")

#     time.sleep(1)