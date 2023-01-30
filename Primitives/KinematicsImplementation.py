import math
import sys
import time
from threading import Thread

from Kinematics.KinematicsClass import Link, Chain
from Primitives.ReplayKinematics import ReplayKinematics
from Kinematics.TrajectoryPlanning import TrajPlanner

sys.path.insert(0, 'home/pi/Documents/koalby-humanoid')

""" DO NOT USE, USE REPLAYPLAYJOSHCOPY.PY FOR NOW """


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

# DH parameters for leg links, used for both legs as same for both
thighLink1 = Link(0, 18.7325, 0, -math.pi / 2, 18.7325)  # cm
shinLink2 = Link(-math.pi / 2, 0, 21.2725, 0, 21.2725)  # cm
ankleLink3 = Link(math.pi / 2, 0, 3.4925, 0, 3.4925)  # cm

leftLegChain = Chain([thighLink1, shinLink2, ankleLink3])
rightLegChain = Chain([thighLink1, shinLink2, ankleLink3])

robot = Robot()
replay = ReplayKinematics(robot.motors)
trajPlanner = TrajPlanner()

# legPositions = replay.recordMotionKinematics()
# replay.legSplitterKinematics()

replay.recordMotionKinematics()

# leftLegPositions = replay.leftLegMotorPositions
# rightLegPositions = replay.rightLegMotorPositions

leftLegPositions = [[0, 0, 0], [math.pi / 2, math.pi / 2, math.pi / 2]]
rightLegPositions = [[0, 0, 0], [math.pi / 2, math.pi / 2, math.pi / 2]]


# def execute_cubic_traj(finalPositionKeys, finalPositionList):  # [[joint1value1, joint2value1, joint3value1], [...]]
#     for position in finalPositionList:
#         positionDictionary = trajPlanner.convert_to_dictionary(finalPositionKeys, position)
#         robot.motorPositionsDict = positionDictionary
#         robot.poseDelay = givenTime / len(finalPositionList) # need to set givenTime as full requested trajectory time
#         time.sleep(robot.poseDelay)

# def execute_cubic_traj(positionList):
#     # replay.playMotion()  # need a version for kinematics???? probably
#     legChoice = float(input("Enter 1 to move left leg or 2 to move right leg:"))
#     if legChoice == 1:
#         positionList = leftLegPositions
#         keys = [13, 14, 15]
#     else:
#         positionList = rightLegPositions
#         keys = [18, 19, 20]
#     initialTime = 0
#     finalTime = float(input("Enter trajectory time (seconds):"))
#     initialVelocity = 0
#     finalVelocity = 0
#     generatedPositionList = trajPlanner.generate_full_cubic_traj_between_two_positions(initialTime, finalTime,
#                                                                                        positionList, initialVelocity,
#                                                                                        finalVelocity)
#     print(generatedPositionList)
#     for position in generatedPositionList:
#         positionDict = trajPlanner.convert_to_dictionary(keys, position)
#         print(positionDict)
#         # robot.motorPositionsDict = positionDict                           UNCOMMENT WHEN READY FOR ROBOT PLUGIN
#         # robot.poseDelay = finalTime - len(positionList)
#         # time.sleep(robot.poseDelay)


# execute_cubic_traj()
# leftFKResult1, leftFKResult2 = leftLegChain.forward_kinematics(leftLegPositions)
# rightFKResult1, rightFKResult2 = rightLegChain.forward_kinematics(rightLegPositions)
#
# leftLegPositionsCheck = leftLegChain.inverse_kinematics_leg(leftFKResult1)
# rightLegPositionsCheck = rightLegChain.inverse_kinematics_leg(rightFKResult1)

# put trajectory planning execution in here

replay.isActive = True

# must restart robot before playing back motion, or change the way prim manager operates (no while loop)
robot.primitives.append(replay)


def Play():
    while True:
        replay.playMotion()
        # replay.poseTime = float(input("Enter pose time (seconds):")) + 0.005
        # replay.poseDelay = float(input("Enter delay between poses (seconds):"))
        # robot.poseTimeMillis = int((replay.poseTime - 0.005) * 1000)
        # replay.replayFilename = str(input("Input saved file name to play back:"))


def Update():
    while True:
        robot.PrimitiveManagerUpdate()


t1 = Thread(target=Update)
t2 = Thread(target=Play)
t1.start()
t2.start()

while True:
    pass
