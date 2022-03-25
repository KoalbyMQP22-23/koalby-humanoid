import sys

from Primitives.ArmMirror import ArmMirror
from Primitives.Dance import Dance

sys.path.insert(0, '/home/pi/Documents/koalby-humanoid')
import time
from threading import Thread
from tkinter import *
from KoalbyHumanoid.robot import Robot

# Start Script
print("Start User Interface")
dance = Dance()
armMirror = None

# Global Boolean to stop all threads
runAll = True


# Primitive Manager Thread
def primitiveUpdateMeth():
    global runAll
    print("Primitive Manager Thread Started")
    while True:
        if dance.isActive or armMirror.isActive:
            print("running")


def startAll():
    global runAll
    runAll = True

def stopAll():
    print("stopping")
    global runAll
    runAll = False


updateT = Thread(target=primitiveUpdateMeth)
updateT.start()


# Dance Thread
def danceMeth():
    print("Dancing Thread Started")
    while True:
        if runAll and dance.isActive:
            print("dancing")
            dance.armDance()
            time.sleep(1)


danceT = Thread(target=danceMeth)
danceT.start()

'''
def armMirrorMeth():
    print("Arm Mirror Thread Started")
    while True:
        if runAll and armMirror.isActive:
            armMirror.armMirror()


armMirrorT = Thread(target=armMirrorMeth)
armMirrorT.start()
'''

# User Interface

def uiupdate():
    window = Tk()
    window.geometry("700x500")

    # Make the buttons

    # b0 = Button(window, text="Stop All Threads and Shutdown", command=stop, activeforeground="red", activebackground="pink", padx=50, pady=25)

    #b1 = Button(window, text="Initialize", command=robot.initialize, activeforeground="black", activebackground="pink", padx=25, pady=25)
    #b2 = Button(window, text="Shutdown", command=robot.shutdown, activeforeground="black", activebackground="pink", padx=25, pady=25)
    b3 = Button(window, text="Start Dance", command=dance.setActive, activeforeground="black", activebackground="pink", padx=25, pady=25)
    b4 = Button(window, text="Stop Dance", command=dance.notActive, activeforeground="black", activebackground="pink", padx=25, pady=25)
    #b5 = Button(window, text="Start Mirror", command=armMirror.setActive, activeforeground="black", activebackground="pink", padx=25, pady=25)
    #b6 = Button(window, text="Stop Mirror", command=armMirror.notActive and stopAll, activeforeground="black", activebackground="pink", padx=25, pady=25)

    # Set button locations
    # b0.place(x=175, y=425)
    #b1.place(x=0, y=0)
    #b2.place(x=0, y=80)
    b3.place(x=150, y=0)
    b4.place(x=150, y=80)
    #b5.place(x=300, y=0)
    #b6.place(x=300, y=80)

    while True:
        window.update()
        window.update_idletasks()


UIThread = Thread(target=uiupdate)
UIThread.start()

while True:
    pass
