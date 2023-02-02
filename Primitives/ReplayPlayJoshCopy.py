import csv
import math
import sys
import time
from threading import Thread

from Kinematics.KinematicsClass import Link, Chain
from Kinematics.TrajectoryPlanning import TrajPlanner
from Primitives.ReplayKinematics import ReplayKinematics
from Primitives.ReplayPrimitive import ReplayPrimitive

sys.path.insert(0, 'home/pi/Documents/koalby-humanoid')

from KoalbyHumanoid.robot import Robot

"""A simple test suite to check pi -> arduino communication and motor control"""

'''
NEXT STEPS:
'''

## Port Finder
import serial.tools.list_ports as ports

com_ports = list(ports.comports())  # create a list of com ['COM1','COM2']
for i in com_ports:
    print(i.device)  # returns 'COMx'

robot = Robot()
replay = ReplayKinematics(robot.motors)
trajPlanner = TrajPlanner()

# robot.poseTimeMillis = int((replay.poseTime - 0.005) * 1000)
# replay.replayFilename = str(input("Input saved file name to play back:"))
replay.isActive = True

# must restart robot before playing back motion, or change the way prim manager operates (no while loop)
robot.primitives.append(replay)


def Play():
    while True:
        rightLegPositions = []
        leftLegPositions = []
        # replay.recordMotionKinematics()                                                       Uncomment to record CSV

        replay.replayFilename = str(input("Input saved file name to play back:"))
        with open(replay.replayFilename) as f:
            csvRecordedPoses = [{k: int(v) for k, v in row.items()}
                                for row in
                                csv.DictReader(f, skipinitialspace=True)]  # parses selected csv file into list of poses
        for poseMotorPositionsDict in csvRecordedPoses:  # for each pose in the list of recorded poses
            if not replay.isActive:
                break
            intermediatePositionLeft = []
            intermediatePositionRight = []
            replay.dummyPosition = poseMotorPositionsDict
            for key in replay.dummyPosition.keys():
                if key == '13' or key == '14' or key == '15':
                    intermediatePositionLeft.append(replay.dummyPosition[key])
                if key == '18' or key == '19' or key == '20':
                    intermediatePositionRight.append(replay.dummyPosition[key])
            leftLegPositions.append(intermediatePositionLeft)
            rightLegPositions.append(intermediatePositionRight)
            # print(poseMotorPositionsDict)
            # time.sleep(replay.poseTime + replay.poseDelay)

        print(rightLegPositions)
        print(leftLegPositions)

        # leftLegPositions = [[0, 0, 0], [math.pi / 2, math.pi / 2, math.pi / 2]]
        # rightLegPositions = [[0, 0, 0], [math.pi / 2, math.pi / 2, math.pi / 2]]

        legChoice = float(input("Enter 1 to move left leg or 2 to move right leg:"))
        if legChoice == 1:
            positionList = leftLegPositions
            keys = [13, 14, 15]
        else:
            positionList = rightLegPositions
            keys = [18, 19, 20]

        t0 = 0
        tf = float(input("Enter trajectory time (seconds):"))
        v0 = 0
        vf = 0


        # iterateThroughThis = []

        iterateThroughThis = trajPlanner.execute_cubic_traj(positionList, keys, t0, tf, v0, vf)
        # intermediateIterateThroughThis = trajPlanner.execute_cubic_traj(positionList, keys, t0, tf, v0, vf)
        # iterateThroughThis.append(intermediateIterateThroughThis)
        # print(term)
        # print(iterateThroughThis)

        # print(iterateThroughThis)

        replay.playMotionKinematics(iterateThroughThis)


def Update():
    while True:
        robot.PrimitiveManagerUpdate()


t1 = Thread(target=Update)
t2 = Thread(target=Play)
t1.start()
t2.start()

while True:
    pass
