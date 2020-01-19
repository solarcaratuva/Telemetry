#handle and store data from xbee here
import random

class Info(object):
    def __init__(self):
        self.mph = random.randint(10,20),
        self.rpm = random.randint(10,20),
        self.miles = random.randint(10,20),

    def to_json(self):
        return {
            "mph": self.mph,
            "rpm": self.rpm,
            "miles": self.miles,
        }