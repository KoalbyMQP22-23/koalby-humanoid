import csv
from Primitives import KoalbyPrimitive
import time


class ReplayPrimitive(KoalbyPrimitive.Primitive):

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

    def playMotion(self):
        """
        iterates through list of recorded poses of entire robot,
        holding each pose for defined pose time.
        """
        with open(self.replayFilename) as f:
            csvRecordedPoses = [{k: int(v) for k, v in row.items()}
                                for row in csv.DictReader(f, skipinitialspace=True)]  # parses selected csv file into list of poses
        for poseMotorPositionsDict in csvRecordedPoses:  # for each pose in the list of recorded poses
            if not self.isActive:
                break
            self.motorPositionsDict = poseMotorPositionsDict
            time.sleep(self.poseTime + self.poseDelay)

    # TODO: make recordMotion based on motor groups for easier recording
    def recordMotion(self):
        """
        Records a series of manually positioned robot poses with a desired number of poses and saves them to a csv file
        """
        self.poseNum = int(input("Input number of poses desired:"))
        for m in self.Motors:
            m.compliantOnOff(1)  # sets all motors in the robot to be compliant for moving to poses
            time.sleep(0.05)  # need delay for comm time
        for poseIndex in range(self.poseNum):  # for each pose from 0 to desired number of poses
            poseMotorPositionsDict = {}
            self.continueSelect = int(input("Type 2 to record to next pose:"))  # wait for user to input "1" in console
            if self.continueSelect != 0:
                time.sleep(0.1)  # delay to allow consistent reading of first motor in first pose
                for m in self.Motors:  # for each motor in Motors list
                    poseMotorPositionsDict[m.motorID] = m.getPosition()  # add the motor ID as key and motor position as value
                self.recordedPoses.append(poseMotorPositionsDict)  # add dictionary of current robot pose to list of recorded poses
            self.continueSelect = 0
            time.sleep(0.01)  # comms buffer delay
        # write dictionary of recorded poses to csv file
        motorIDHeaders = self.recordedPoses[0].keys()
        motionFile = open(str(input("Input saved file name:")), "w")  # request a filename
        dict_writer = csv.DictWriter(motionFile, motorIDHeaders)
        dict_writer.writeheader()
        dict_writer.writerows(self.recordedPoses)
        motionFile.close()
        for m in self.Motors:
            m.compliantOnOff(0)  # set motors back to non-compliant for use elsewhere
            time.sleep(0.05)  # need delay for comm time

    def change(self):
        if self.isActive:
            self.isActive = False
        else:
            self.isActive = True

    def setActive(self):
        self.isActive = True

    def notActive(self):
        self.isActive = False
