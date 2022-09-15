#
# 3 dicts - motors, sensors, externals
# need to be dicts of key and list of values
# get primitive attach primitive to robot add itself to robot primitive list
# also a remove primitive function
# timing method
import threading


class Primitive:

    def __init__(self):
        self.motorPositionsDict = {}  # dictionary holding motorIDs and their relevant data
        self.sensorDict = {}  # dictionary holding sensorIDs and their relevant data
        self.isActive = False

    def get_motor_dict(self):
        return self.motorPositionsDict

    def timer(self, duration):
        timer = threading.Timer(duration, '''Function''')
        timer.start()  # after 'duration' seconds, 'removePrimitive' will be called


