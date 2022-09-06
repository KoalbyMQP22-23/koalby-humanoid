import sys
from threading import Thread

from Primitives.ReplayPrimitive import ReplayPrimitive

sys.path.insert(0, 'home/pi/Documents/koalby-humanoid')

from KoalbyHumanoid.robot import Robot

"""A simple test suite to check pi -> arduino communication and motor control"""

'''
NEXT STEPS:
'''

robot = Robot()
replay = ReplayPrimitive(robot.motors)
replay.poseTime = float(input("Enter pose time (seconds):")) + 0.005
replay.poseDelay = float(input("Enter delay between poses (seconds):"))
robot.poseTimeMillis = int((replay.poseTime - 0.005)*1000)
replay.replayFilename = str(input("Input saved file name to play back:"))
replay.isActive = True

# must restart robot before playing back motion, or change the way prim manager operates (no while loop)
robot.primitives.append(replay)


def Play():
    while True:
        replay.playMotion()
        replay.poseTime = float(input("Enter pose time (seconds):")) + 0.005
        replay.poseDelay = float(input("Enter delay between poses (seconds):"))
        robot.poseTimeMillis = int((replay.poseTime - 0.005) * 1000)
        replay.replayFilename = str(input("Input saved file name to play back:"))


def Update():
    while True:
        robot.PrimitiveManagerUpdate()


t1 = Thread(target=Update)
t2 = Thread(target=Play)
t1.start()
t2.start()

while True:
    pass
