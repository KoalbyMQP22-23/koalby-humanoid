import time

import ArduinoSerial

# import config

"""The Motor class hold all information for an abstract motor on the physical robot. It is used to interface with the
arduino which directly controls the motors"""


class Motor(object):

    def __init__(self, _motorID, angleLimit, name, serial):
        self.motorID = _motorID
        self.angle_limit = angleLimit
        self.name = name

        self.arduino_serial = serial

    def getPosition(self):
        """reads the motor's current position from the arduino and returns the value in degrees"""
        idArr = [5, self.motorID]
        self.arduino_serial.send_command(','.join(map(str, idArr)) + ',')
        # print("get position", ','.join(map(str, idArr))+',')
        currentPosition = self.arduino_serial.read_command()
        # print(currentPosition)
        return currentPosition

    def setPositionPos(self, position):
        """sends a desired motor position to the arduino"""
        position = int(position)
        idPosArr = [10, self.motorID, position]
        # print("send pos", ','.join(map(str, idPosArr))+',')
        self.arduino_serial.send_command(','.join(map(str, idPosArr)) + ',')
        # print(ArduinoSerial.read_command())

    def setPositionTime(self, position, time):
        """sends a desired motor position to the arduino <to be executed in a set amount of time?>"""
        idPosTimeArr = [11, self.motorID, position, time]
        # testArr = [self.motorID, position]
        # print(','.join(map(str, testArr)))
        self.arduino_serial.send_command(','.join(map(str, idPosTimeArr)) + ',')

    def torqueOnOff(self, toggle):
        """turns the torque of a motor on or off based on a 1 or 0 input and sends this to the arduino"""
        idBoolArr = [20, self.motorID, toggle]
        self.arduino_serial.send_command(','.join(map(str, idBoolArr)) + ',')

    def compliantOnOff(self, toggle):
        """turns the compliancy of a motor on or off based on a 1 or 0 input and sends this to the arduino"""
        idBoolArr = [21, self.motorID, toggle]
        self.arduino_serial.send_command(','.join(map(str, idBoolArr)) + ',')
