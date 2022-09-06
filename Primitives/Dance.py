"""
Dance Primitive

    DanceToBeat()
        cause robot to move rhythmically in response to a beats per minute (BPM) input
"""
import random
import threading
from threading import Thread
import time

from KoalbyHumanoid.config import motors
from Primitives import KoalbyPrimitive


class Dance(KoalbyPrimitive.Primitive):

    def __init__(self):
        super().__init__()  # inheritance
        self.motorPositionsDict = {}
        self.isActive = False

    def armDance(self):
        self.motorPositionsDict = {}  # Clear the dictionary
        for index in range(0, 8):  # Set depth to run in config file (0-4 is right arm motors)
            motorID = motors[index][0]  # Get motor ID
            motorPos = random.randrange(0, 100, 10)  # Generate random positions between 0 and 100
            self.motorPositionsDict[motorID] = motorPos  # add position to dictionary

    def change(self):
        if self.isActive:
            self.isActive = False
        else:
            self.isActive = True

    def setActive(self):
        self.isActive = True

    def notActive(self):
        self.isActive = False

    def timer(self, duration):
        timer = threading.Timer(duration, self.armDance())
        timer.start()  # after 'duration' seconds, 'removePrimitive' will be called
