#handle and store data from xbee here
import random
from datetime import datetime

class Info(object):
    def __init__(self):

        self.mph = random.randint(10,20);
        self.rpm = random.randint(10,20),
        self.miles = random.randint(10,20);
        self.socTime = str(datetime.now().strftime("%H:%M:%S")),
        self.socVal = random.randint(10,200);


    def to_json(self):
        return {
            "mph": self.mph,
            "rpm": self.rpm,
            "miles": self.miles,
            "socTime": self.socTime,
            "socVal": self.socVal,

        }
    
    def change(self):
        self.mph = random.randint(10,200);