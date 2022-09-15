import time

from KoalbyHumanoid.Robot import Robot
from threading import Thread

from Primitives.Dance import Dance

robot = Robot()
dance = Dance()
robot.primitives.append(dance)


def update():
    while True:
        robot.PrimitiveManagerUpdate()


def arm_follow():
    while True:
        dance.arm_dance()
        time.sleep(1)


t1 = Thread(target=update)
t2 = Thread(target=arm_follow)
t1.start()
t2.start()


while True:
    pass
