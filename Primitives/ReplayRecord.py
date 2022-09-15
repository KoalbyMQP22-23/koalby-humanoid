from KoalbyHumanoid.Robot import Robot
from Primitives.ReplayPrimitive import ReplayPrimitive

robot = Robot()
replay = ReplayPrimitive(robot.motors)
replay.record_motion()
