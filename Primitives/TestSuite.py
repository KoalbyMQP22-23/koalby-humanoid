import time

from KoalbyHumanoid.robot import Robot
from threading import Thread

from Primitives.ArmMirror import ArmMirror
from Primitives.Dance import Dance

robot = Robot()
dance2 = Dance()
robot.primitives.append(dance2)


def update():
    while True:
        robot.PrimitiveManagerUpdate()


def arm_Follow():
    while True:
        dance2.armDance()
        time.sleep(1)


t1 = Thread(target=update)
t2 = Thread(target=arm_Follow)
t1.start()
t2.start()


while True:
    pass
