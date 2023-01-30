from abc import ABC, abstractmethod, abstractproperty

from KoalbyHumanoid.Robot import Robot


class Action(ABC):

    robot = Robot()


    def __init__(self, motors):
        super().__init__()  # inheritance
        self.Motors = motors
        self.recordedPoses = list()
        self.continueSelect = 0
        self.poseNum = 0
        self.poseTime = 0.0
        self.poseDelay = 0.0
        self.motorPositionsDict = {}
        self.isActive = False
        self.replayFilename = ""



    @abstractmethod
    def play(self):
        pass


    def update(self):
        pass
