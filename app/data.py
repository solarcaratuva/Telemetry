#handle and store data from xbee here
import random
import msgpack
from openpyxl import load_workbook
import serial
import time


class Info(object):
    def __init__(self):
        self.workbook = load_workbook(filename="app/data_label.xlsx")
        self.ws = self.workbook.active
        self.column = (self.ws['G'])[1:]
        self.labels = {}
        self.nonbinary_labels = set(["b", "k"])

        #identifies array label and adds value to it appropriately
        for i in self.column:
            if (i.value not in self.labels) and (i.value is not None):
                self.labels[i.value] = 1
            elif (i.value is not None):
                self.labels[i.value] += 1
        
        self.data_values = {}
        for label in self.labels:
            num = self.labels[label]
            if label not in self.data_values:
                self.data_values[label] = [-1 for i in range(num)]
        self.gen_random()


    def gen_random(self):
        for label in self.labels:
            num = self.labels[label]
            for i in range(num):
                if label not in self.nonbinary_labels:
                    self.data_values[label][i] = random.randint(0, 1)
                else:
                    self.data_values[label][i] = random.randint(10, 20)


    def to_json(self):
        msgpack_data = {}
        for label in self.labels:
            num = self.labels[label]
            data_arr = []
            for i in range(num):
                data_arr.append(self.data_values[label][i])
            msgpack_data[label] = data_arr
        
        return msgpack.packb(msgpack_data, use_bin_type=True)


    def output(self, port):
        ser = serial.Serial(port, 115200, timeout=1)

        while True:
            d = self.to_json()
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
