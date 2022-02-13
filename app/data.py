#handle and store data from xbee here
import random
import msgpack
from openpyxl import load_workbook
import serial
import time
import json


class Info(object):
    def __init__(self):
        # self.workbook = load_workbook(filename="app/data_label.xlsx")
        # self.ws = self.workbook.active
        self.json_data = json.load(open("app/data.json"))
        self.data_values = {}
        self.data_types = {}

        #identifies array label and adds value to it appropriately
        for key in self.json_data:
            label, typ = key.strip(), self.json_data[key].strip()
            self.data_values[label] = 0
            self.data_types[label] = typ
        
        self.gen_random()


    def get_random_val(self, typ):
        if typ == 'bool':
            if random.random() < 0.5:
                return True
            return False
        elif typ == 'int':
            return random.randint(10, 20)
        elif typ == 'float':
            return random.randint(1000, 2000) / 100
        print("ERROR UNKNOWN TYPE:", typ)
        assert(False)


    def gen_random(self):
        for label in self.data_values:
            self.data_values[label] = self.get_random_val(self.data_types[label])


    def output(self, port):
        ser = serial.Serial(port, 115200, timeout=1)

        while True:
            d = self.data_values
            print(type(d))
            ser.write(d)
            print(d)
            print(msgpack.unpackb(d,raw="False"))
            time.sleep(.01)
            print("sent")



if __name__ == "__main__":
    serial_port = 'ttyS10'
    k = Info()
    k.output(serial_port)
