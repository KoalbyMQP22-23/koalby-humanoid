import csv
import time

from KoalbyHumanoid.RobotTest import Robot


robot = Robot()

while True:

    motor_positions_dict = {}
    poseTime = float(input("Enter pose time in seconds"))
    poseDelay = float(input("Enter delay between pose time in seconds"))
    fileName = "poses/" + str(input("Input saved file name to play back:"))
    robot.poseTimeMillis = int((poseTime - 0.005) * 1000)


    def play_motion():
        with open(fileName) as f:
            csv_recorded_poses = [{k: int(v) for k, v in row.items()}
                                  for row in
                                  csv.DictReader(f, skipinitialspace=True)]
        for poseMotorPositionsDict in csv_recorded_poses:
            robot.motor_positions_dict = poseMotorPositionsDict
            time.sleep(poseTime + poseDelay)

        robot.update_motors()

    play_motion()



