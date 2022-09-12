import sys

from Primitives.ReplayPrimitive import ReplayPrimitive

sys.path.insert(0, 'poses/home/pi/Documents/koalby-humanoid')

from KoalbyHumanoid.robot import Robot

robot = Robot()
replay = ReplayPrimitive(robot.motors)
replay.recordMotion()

