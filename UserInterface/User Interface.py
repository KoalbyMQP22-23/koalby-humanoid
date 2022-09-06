import sys

from Primitives.ArmMirror import ArmMirror
from Primitives.Dance import Dance
from Primitives.ReplayPrimitive import ReplayPrimitive

sys.path.insert(0, '/home/pi/Documents/koalby-humanoid')
import time
from threading import Thread
from tkinter import *
from KoalbyHumanoid.robot import Robot

# Start Script
print("Start User Interface")

b1, b2, b3, b4, b5, b6, b7, b8, b9, b10 = Button(), Button(), Button(), Button(), Button(), Button(), Button(), Button(), Button(), Button()  # Create Global buttons so all functions can use them
robot = Robot()
dance = Dance()
replay = ReplayPrimitive(robot.motors)
armMirror = ArmMirror(robot.motors[0:3], robot.motors[4:7])  # Arm Mirror created with left and right arm motor groups


# Initialize the Robot Command
def init():
    for prim in robot.primitives:  # Set all primitives in robot list to not active
        prim.notActive()
    robot.primitives.clear()  # Clear the robot list of primitives
    allButtonsOff()  # Set all buttons to the color red
    time.sleep(0.5)  # Delay so the primitive manager can have time to stop sending commands to prevent a serial timeout error
    robot.initialize()


# Shutdown the robot (Turn off all motors)
def shutdown():
    for prim in robot.primitives:  # Set all primitives in robot list to not active
        prim.notActive()
    robot.primitives.clear()  # Clear the robot list of primitives
    allButtonsOff()  # Set all buttons to the color red
    time.sleep(0.5)  # Delay so the primitive manager can have time to stop sending commands to prevent a serial timeout error
    robot.shutdown()


# Primitive Manager Thread
def primitiveUpdateMeth():
    print("Primitive Manager Thread Started")
    while True:
        if dance.isActive or armMirror.isActive or replay.isActive:  # If any of the primitives are active then the thread will run the primitive manager update function in robot
            robot.PrimitiveManagerUpdate()


# Start Primitive Manager Thread
primitiveUpdateT = Thread(target=primitiveUpdateMeth)
primitiveUpdateT.start()


# Dance Thread
def danceMeth():
    print("Dancing Thread Started")
    while True:
        if dance.isActive:
            robot.poseTimeMillis = 1000
            dance.armDance()
            time.sleep(1)


def danceSetup():
    if dance.isActive:
        robot.removePrimitive(dance)
        dance.isActive = False
        allButtonsOff()
    else:
        robot.addPrimitive(dance)
        dance.isActive = True
        b3.config(bg="green")


# Start Dance Thread
danceT = Thread(target=danceMeth)
danceT.start()

'''
*** This method does not work on the Python side, but does work on the Arduino side

# Arm Mirror Thread
def armMirrorMeth():
    print("Arm Mirror Thread Started")
    while True:
        if armMirror.isActive:
            armMirror.armMirror()


def armMirrorSetup():
    if armMirror.isActive:
        robot.removePrimitive(armMirror)
        armMirror.isActive = False
        allButtonsOff()
    else:
        robot.addPrimitive(armMirror)
        armMirror.isActive = True
        b4.config(bg="green")


# Start Arm Mirror Thread
armMirrorT = Thread(target=armMirrorMeth)
armMirrorT.start()
'''


# Replay Thread
def replayMeth():
    print("Replay Thread Started")
    while True:
        if replay.isActive:
            replay.playMotion()  # Replay


def replaySetup(posTime, posDelay, filename):
    # Setup the replay object's parameters
    replay.poseTime = posTime + 0.005
    replay.poseDelay = posDelay
    robot.poseTimeMillis = int((replay.poseTime - 0.005) * 1000)
    replay.replayFilename = filename

    if replay.isActive:
        replay.isActive = False
        allButtonsOff()  # Turn buttons red
        robot.removePrimitive(replay)  # Remove primitive from robot list


    else:
        replay.isActive = True
        robot.addPrimitive(replay)


# Start Replay Thread
replayT = Thread(target=replayMeth)
replayT.start()

'''
*** There needs to be a function linked to each button in the UI and the Tkinter library does not allow functions in the button command to pass fields.
'''


# Clap 0.2 0.1, Dab 0.1 0, Macerena 0.5 0.2, Shake 0.2 0 , Extend 0.5 0, Wave 0.3 0
def clap():
    b5.config(bg="green")
    replaySetup(0.5, 0.5, "../Primitives/clapCycle")


def dab():
    b6.config(bg="green")
    replaySetup(0.3, 0.5, "../Primitives/dab")


def macarena():
    b7.config(bg="green")
    replaySetup(0.5, 1, "../Primitives/macarena")


def shake():
    b10.config(bg="green")
    replaySetup(0.2, 0.5, "../Primitives/shakeRightHand")


def extend():
    b9.config(bg="green")
    replaySetup(0.5, 0.5, "../Primitives/extendRightArm")


def wave():
    b8.config(bg="green")
    replaySetup(0.3, 0.5, "../Primitives/wave")


# User Interface

def UI():
    global b1, b2, b3, b4, b5, b6, b7, b8, b9, b10  # Global Variable for each button so other methods can control button fields.

    # Create the Window Tkinter object
    window = Tk()
    window.geometry("800x500")

    # Make the buttons
    b1 = Button(window, text="Initialize", command=init, bg="red", activeforeground="black", activebackground="green", padx=25, pady=25)
    b2 = Button(window, text="Shutdown", command=shutdown, bg="red", activeforeground="black", activebackground="green", padx=25, pady=25)
    b3 = Button(window, text="Dance Toggle", command=danceSetup, bg="red", activeforeground="black", activebackground="green", padx=25, pady=25)
    # b4 = Button(window, text="Mirror Toggle", command=armMirrorSetup, bg="red", activeforeground="black", activebackground="green", padx=25, pady=25)
    b5 = Button(window, text="Clap Toggle", command=clap, bg="red", activeforeground="black", activebackground="green", padx=25, pady=25)
    b6 = Button(window, text="Dab Toggle", command=dab, bg="red", activeforeground="black", activebackground="green", padx=25, pady=25)
    b7 = Button(window, text="Macarena Toggle", command=macarena, bg="red", activeforeground="black", activebackground="green", padx=20, pady=25)
    b8 = Button(window, text="Wave Toggle", command=wave, bg="red", activeforeground="black", activebackground="green", padx=25, pady=25)
    b9 = Button(window, text="Extend Toggle", command=extend, bg="red", activeforeground="black", activebackground="green", padx=25, pady=25)
    b10 = Button(window, text="Shake Toggle", command=shake, bg="red", activeforeground="black", activebackground="green", padx=25, pady=25)

    # Set button locations
    b1.place(x=0, y=0)
    b2.place(x=0, y=80)
    b3.place(x=150, y=0)
    b4.place(x=150, y=80)
    b5.place(x=300, y=0)
    b6.place(x=300, y=80)
    b7.place(x=450, y=0)
    b8.place(x=450, y=80)
    b9.place(x=600, y=0)
    b10.place(x=600, y=80)

    while True:
        window.update()
        window.update_idletasks()


def allButtonsOff():
    global b1, b2, b3, b4, b5, b6, b7, b8, b9, b10
    b1.config(bg="red")
    b2.config(bg="red")
    b3.config(bg="red")
    b4.config(bg="red")
    b5.config(bg="red")
    b6.config(bg="red")
    b7.config(bg="red")
    b8.config(bg="red")
    b9.config(bg="red")
    b10.config(bg="red")


# Start UI Thread
UIThread = Thread(target=UI)
UIThread.start()


# Infinite loop so all threads will continue to run off of main thread
while True:
    pass
