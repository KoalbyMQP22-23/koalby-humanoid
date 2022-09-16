"""
Dance Primitive

    DanceToBeat()
        cause robot to move rhythmically in response to a beats per minute (BPM) input
"""
import random

from KoalbyHumanoid.Config import motors
from Primitives import KoalbyPrimitive


class Dance(KoalbyPrimitive.Primitive):

    def __init__(self):
        super().__init__()  # inheritance  # why is this here?
        self.motorPositionsDict = {}
        self.isActive = False

    def arm_dance(self):
        self.motorPositionsDict = {}  # Clear the dictionary
        for index in range(0, 8):  # Set depth to run in config file (0-4 is right arm motors)
            motor_id = motors[index][0]  # Get motor ID
            motor_pos = random.randrange(0, 100, 10)  # Generate random positions between 0 and 100
            self.motorPositionsDict[motor_id] = motor_pos  # add position to dictionary

    def change_active_state(self):
        if self.isActive:
            self.isActive = False
        else:
            self.isActive = True

    def timer(self, duration):
        pass
