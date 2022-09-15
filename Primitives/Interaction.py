import time
import KoalbyHumanoid.Robot as Robot

"""
Interaction Primitive:
*** may break up into multiple primitives ***

    ArmMirror()
        allows user to move left arm such that the right arm copies the left arm motion

    ManualArmControlHold()
        allows user to move arms to positions and robot will then hold arm at those positions
        can then move arm again and robot will become compliant to do so

    ManualArmControlCopy()
        allows user to make a motion with the arms, the robot will then copy this motion in a loop until stopped
        example: user moves arm in a waving pattern, robot will then loop this wave until told to stop
"""
robot = Robot.Robot()


def arm_mirror_old():
    for m in robot.r_arm:
        m.torqueOnOff(0)

    try:
        while True:
            r_arm_angles = robot.r_arm_chain.joints_position
            print("Right arm: ", r_arm_angles)
            for m, pos in list(zip(robot.l_arm_chain.motors, r_arm_angles)):
                if 'l_' in m.name:
                    m.setPositionPos(pos)
            time.sleep(1)

    # Close properly the object when finished
    except KeyboardInterrupt:
        robot.powerSwitch(100)


def arm_mirror_simple_old():
    for m in robot.r_arm:
        m.torqueOnOff(0)
    try:
        while True:
            r_pos = robot.r_shoulder_y.getPosition()
            # print(r_pos)

            robot.l_shoulder_y.setPositionPos(r_pos)
    except KeyboardInterrupt:
        robot.powerSwitch(100)


# Ian Code. Temporary putting here
def arm_follow_test():
    # Left arm is compliant, right arm is active
    '''for m in robot.l_arm:
        m.torqueOnOff(1)'''

    for m in robot.r_arm:
        m.torqueOnOff(0)

    # The torso itself must not be compliant
    '''for m in robot.torso:
        m.torqueOnOff(1)'''

    target_delta = [0, -0.1, 0]
    try:
        while True:
            follow_hand(target_delta)
            time.sleep(1)

    # Close properly the object when finished
    except KeyboardInterrupt:
        robot.powerSwitch(100)


def follow_hand(delta):
    """Tell the left hand to follow the right hand"""
    left_arm_position = robot.r_arm_chain.position + delta
    robot.l_arm_chain.goto(left_arm_position, 0.5, wait=True)


def arm_replay_test():
    try:
        while True:
            # Torque off
            for m in robot.r_arm:
                m.torqueOnOff(0)
            print("Torque off. Position Arm now")
            time.sleep(5)

            pos = robot.r_arm_chain.position
            print("Arm at: ", pos, ". Release arm now")
            time.sleep(3)

            # Torque on
            for m in robot.r_arm:
                m.torqueOnOff(1)

            print("Torque on. Moving soon")
            time.sleep(1)

            robot.r_arm_chain.goto(pos, 0.5, wait=True)
            time.sleep(1)
            print("Arm Holding Position", robot.r_arm_chain.position)
            time.sleep(4)

    # Close properly the object when finished
    except KeyboardInterrupt:
        robot.powerSwitch(100)
