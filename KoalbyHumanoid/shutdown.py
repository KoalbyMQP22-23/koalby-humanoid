import sys, os

sys.path.insert(0, '/home/pi/Documents/koalby-humanoid')

from KoalbyHumanoid.robot import Robot

robot = Robot()
robot.shutdown()
