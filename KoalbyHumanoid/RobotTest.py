"""
To be used for robot instantiation.
Possible functionalities:
    - call robot URDF body layout file and call kinematic and IK methods
    - set up config file and motor groupings
    - handle sensor layout set up
    - handle full robot-wide commands such as "shutdown"
"""
import sys
import ArduinoSerial
from KoalbyHumanoid.Motor import Motor
import KoalbyHumanoid.Config as config
from collections import defaultdict

sys.path.insert(0, '/home/pi/Documents/koalby-humanoid')


class Robot(object):

    def __init__(self):
        self.arduino_serial = ArduinoSerial.ArduinoSerial()
        self.primitives = []
        self.primitiveMotorDict = {}
        self.poseTimeMillis = 1000
        self.motors = self.motorsInit()
        self.motor_groups_init()
        self.arduino_serial.send_command('1,')  # This initializes the robot with all the initial motor positions
        print("Robot Created and Initialized")

    def motors_init(self):
        motors = list()
        for motorConfig in config.motors:
            motor = Motor(motorConfig[0], motorConfig[1], motorConfig[3], self.arduino_serial)
            setattr(Robot, motorConfig[3], motor)
            motors.append(motor)
        return motors

    def update_motors(self):
        """
        Take the primitiveMotorDict and send the motor values to the robot
        """
        for key, value in self.primitiveMotorDict.items():  # value is never used
            if self.primitiveMotorDict[key] == "":
                self.primitiveMotorDict[key] = 0
            for motor in self.motors:
                if str(motor.motorID) == str(key):
                    motor.setPositionTime(self.primitiveMotorDict[key], self.poseTimeMillis)

    def motor_groups_init(self):
        i = 0
        for row in config.motorGroups:
            group = list()
            for row2 in row[1]:
                motor = Motor(row2[0], row2[1], row2[3], self.arduino_serial)
                group.append(motor)
            setattr(Robot, config.motorGroups[i][0], group)
            i += 1
