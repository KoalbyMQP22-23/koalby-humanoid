"""
To be used for robot instantiation.
Possible functionalities:
    - call robot URDF body layout file and call kinematic and IK methods
    - set up config file and motor groupings
    - handle sensor layout set up
    - handle full robot-wide commands such as "shutdown"
"""
import sys, os

sys.path.insert(0, '/home/pi/Documents/koalby-humanoid')
import ArduinoSerial
from KoalbyHumanoid.motor import Motor
from Kinematics.IK import IKChain
import KoalbyHumanoid.config as config
from collections import defaultdict
from threading import Thread


class Robot(object):

    def __init__(self):
        self.arduino_serial = ArduinoSerial.ArduinoSerial()
        self.primitives = []
        self.primitiveMotorDict = {}
        self.poseTimeMillis = 1000
        self.motors = self.motorsInit()
        self.motorGroupsInit()
        self.arduino_serial.send_command('1,')  # This initializes the robot with all the initial motor positions
        print("Robot Created and Initialized")
        # = Thread(target=self.primiti)
        # t2.start()

        # self.arduino_serial = [] # Fake assignment for testing without robot.
        # If it reaches 'AttributeError: 'list' object has no attribute 'send_command'' Then test on robot

        """
        # Change the tip later if needed
        self.l_arm_chain = IKChain.from_poppy_creature(self, motors=self.torso + self.l_arm, passiv=self.torso,
                                                       tip=[0, 0.18, 0])
        self.r_arm_chain = IKChain.from_poppy_creature(self, motors=self.torso + self.r_arm, passiv=self.torso,
                                                       tip=[0, 0.18, 0])
    """

    def initialize(self):
        """sends command to the arduino to shutdown all motors on the entire robot and turn their LEDs red"""
        cmd = "1,"
        self.arduino_serial.send_command(cmd)

    def shutdown(self):
        """sends command to the arduino to shutdown all motors on the entire robot and turn their LEDs red"""
        cmd = "100,"
        self.arduino_serial.send_command(cmd)

    def motorsInit(self):
        motors = list()
        for motorConfig in config.motors:
            motor = Motor(motorConfig[0], motorConfig[1], motorConfig[3], self.arduino_serial)
            setattr(Robot, motorConfig[3], motor)
            motors.append(motor)
        return motors

    def updateMotors(self):
        '''
        Take the primitiveMotorDict and send the motor values to the robot
        '''
        for key, value in self.primitiveMotorDict.items():
            if self.primitiveMotorDict[key] == "":  # Ensures the key's value is not an empty string and makes it 0 if it is
                self.primitiveMotorDict[key] = 0
            for motor in self.motors:
                if str(motor.motorID) == str(key):
                    motor.setPositionTime(self.primitiveMotorDict[key], self.poseTimeMillis)

    def PrimitiveManagerUpdate(self):
        '''
        Take list of active primitives which will come from UI
        Look at motor Dict from primitives.
        All primitive update functions need to have a dict of motor IDs and setPositions
        '''

        # If there is only 1 primitive in active list, return primitive's dictionary
        if len(self.primitives) == 1:
            self.primitiveMotorDict = self.primitives[0].getMotorDict()
            #print("Update")
            #print(self.primitiveMotorDict)
            self.updateMotors()  # send new dict to motors
            return self.primitiveMotorDict

        primitiveDicts = []
        for primitive in self.primitives:
            #print("Get Dictionary")
            #print(primitive.getMotorDict())
            primitiveDicts.append(primitive.getMotorDict())  # Add primitive dictionary to primitiveDicts

        # create new dictionary with 1 key value and a list of motor positions
        mergedDict = defaultdict(list)  # Create a default list dictionary empty.
        for dict in primitiveDicts:
            for key, value in dict.items():
                mergedDict[key].append(value)

        # for each key average motor positions and return key value with the average value
        for key, value in mergedDict.items():
            finalMotorValue = 0
            for motorValue in mergedDict[key]:
                finalMotorValue = motorValue + finalMotorValue
            self.primitiveMotorDict[key] = finalMotorValue / len(mergedDict[key])  # average values

        self.updateMotors()  # send new dict to motors

        return self.primitiveMotorDict

    def motorGroupsInit(self):
        i = 0
        for row in config.motorGroups:
            group = list()
            for row2 in row[1]:
                motor = Motor(row2[0], row2[1], row2[3], self.arduino_serial)
                group.append(motor)
            setattr(Robot, config.motorGroups[i][0], group)
            i += 1

    def close(self):
        # Can add other stuff here if we need to handle incomplete statement sending
        self.shutdown()

    def addPrimitive(self, primitive):
        self.primitives.append(primitive)

    def removePrimitive(self, primitive):
        self.primitives.remove(primitive)

