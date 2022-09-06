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
replay.isActive = True

# must restart robot before playing back motion, or change the way prim manager operates (no while loop)
robot.primitives.append(replay)


def Play():
    while True:
        replay.replayFilename = str(input("Input saved file name to play back: "))
        replay.poseTime = float(input("Enter pose time (seconds): ")) + 0.005
        # replay.poseTime = 0.505  # use instead of line above if you want quicker manual swapping between poses
        replay.poseDelay = float(input("Enter delay between poses (seconds): "))
        # replay.poseDelay = 0  # use instead of line above if you want quicker manual swapping between poses
        robot.poseTimeMillis = int((replay.poseTime - 0.005) * 1000)
        iterations = int(input("number of iterations: "))
        for i in range(iterations):
            replay.playMotion()


def Update():
    while True:
        robot.PrimitiveManagerUpdate()


t1 = Thread(target=Update)
t2 = Thread(target=Play)
t1.start()
t2.start()

while True:
    pass
