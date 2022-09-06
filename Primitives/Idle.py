"""
Idle Primitive

Causes Koalby to move/sway slightly in an idle animation
"""

from Primitives import KoalbyPrimitive


class Idle(KoalbyPrimitive.Primitive):

    def __init__(self):
        super().__init__()  # inheritance
        self.motorPositionsDict = {3: 50,
                                   2: 50,
                                   1: 50,
                                   0: 50}

    def changePos(self):
        self.motorPositionsDict = {3: 0,
                                   2: 0,
                                   1: 0,
                                   0: 0}


'''
import random
from KoalbyHumanoid.config import motors
from Primitives import KoalbyPrimitive

class Idle(KoalbyPrimitive.Primitive):

    def __init__(self, motors):
        super().__init__()  # inheritance
        self.motorPositionsDict = {}
        self.isActive = True

    def idleAnimation(self):
        # Currently only moves the arms
        self.motorPositionsDict = {}  # Clear the dictionary
        for index in range(0, 8):  # Set depth to run in config file (0-4 is right arm motors)
            motorID = motors[index][0]  # Get motor ID
            motorPos = random.randrange(0, 15, 5)  # Generate random positions between 0 and 100
            self.motorPositionsDict[motorID] = motorPos  # add position to dictionary
'''
