import numpy as np
import mediapipe as mp
import cv2
import win32api
import win32con
import time
import pydirectinput as py
import math
import zmq
import random
import sys
import time

#Set up subscriber
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
print("connected")
socket.setsockopt_string(zmq.SUBSCRIBE, 'turnbody_swimming_eating')

#the functions
def checkIpressed():
    if win32api.GetKeyState(0x49) < 0:
        return True
    else:
        return False
def checkJpressed():
    if win32api.GetKeyState(0x4A) < 0:
        return True
    else:
        return False
def checkKpressed():
    if win32api.GetKeyState(0x4B) < 0:
        return True
    else:
        return False
def checkLpressed():
    if win32api.GetKeyState(0x4C) < 0:
        return True
    else:
        return False

def releaseI():
    py.keyUp("i")
def releaseJ():
    py.keyUp("j")
def releaseK():
    py.keyUp("k")
def releaseL():
    py.keyUp("l")

def pressI():
    py.keyDown("i")
def pressJ():
    py.keyDown("j")
def pressK():
    py.keyDown("k")
def pressL():
    py.keyDown("l")
def turnbody():
    #old
    """
    if abs(left_hand_x - left_elbow_x) < 0.08 and abs(left_hand_y - left_elbow_y) < 0.08:
        if win32api.GetKeyState(0x4C) >= 0 and win32api.GetKeyState(0x49) >= 0 and win32api.GetKeyState(
                0x4A) >= 0 and win32api.GetKeyState(0x4B) >= 0:
            pass
        else:
            py.keyUp("l")
            py.keyUp("i")
            py.keyUp("k")
            py.keyUp("j")
    """
    #new
    if stop_turning_body == 1:

        #from N
        if checkIpressed() == True and checkJpressed() == False and checkKpressed() == False and checkLpressed() == False:
            py.keyUp("i")
        #from W
        elif checkIpressed() == False and checkJpressed() == True and checkKpressed() == False and checkLpressed() == False:
            py.keyUp("j")
        #from S
        elif checkIpressed() == False and checkJpressed() == False and checkKpressed() == True and checkLpressed() == False:
            py.keyUp("k")
        #from E
        elif checkIpressed() == False and checkJpressed() == False and checkKpressed() == False and checkLpressed() == True:
            py.keyUp("l")
        #from NW
        elif checkIpressed() == True and checkJpressed() == True and checkKpressed() == False and checkLpressed() == False:
            py.keyUp("i")
            py.keyUp('j')
        # from SW
        elif checkIpressed() == False and checkJpressed() == True and checkKpressed() == True and checkLpressed() == False:
            py.keyUp("k")
            py.keyUp('j')
        # from SE
        elif checkIpressed() == False and checkJpressed() == False and checkKpressed() == True and checkLpressed() == True:
            py.keyUp("k")
            py.keyUp('l')
        # from NE
        elif checkIpressed() == True and checkJpressed() == False and checkKpressed() == False and checkLpressed() == True:
            py.keyUp("i")
            py.keyUp('l')

    # NE
    elif 67.5 > degree_theta > 22.5:
        if checkJpressed() == True:
            releaseJ()
        if checkKpressed() == True:
            releaseK()
        if checkIpressed() == False:
            pressI()
        if checkLpressed() == False:
            pressL()

    # N direction
    elif 112.5 > degree_theta > 67.5:
        if checkKpressed() == True:
            releaseK()
        if checkJpressed() == True:
            releaseJ()
        if checkLpressed() == True:
            releaseL()
        if checkIpressed() == False:
            pressI()
    # NW region
    elif 157.5 > degree_theta > 112.5:
        if checkKpressed() == True:
            releaseK()
        if checkLpressed() == True:
            releaseL()
        if checkIpressed() == False:
            pressI()
        if checkJpressed() == False:
            pressJ()

    # W direction
    elif (202.5 > degree_theta > 157.5):
        if checkIpressed() == True:
            releaseI()
        if checkLpressed() == True:
            releaseL()
        if checkKpressed() == True:
            releaseK()
        if checkJpressed() == False:
            pressJ()

    # SW region:
    elif (247.5 > degree_theta > 202.5):
        if checkIpressed() == True:
            releaseI()

        if checkLpressed() == True:
            releaseL()

        if checkJpressed() == False:
            pressJ()

        if checkKpressed() == False:
            pressK()
    # S direction
    elif 292.5 > degree_theta > 247.5:
        if checkIpressed() == True:
            releaseI()
        if checkLpressed() == True:
            releaseL()
        if checkJpressed() == True:
            releaseJ()
        if checkKpressed() == False:
            pressK()
    # SE region
    elif 337.5 > degree_theta > 292.5:
        if checkIpressed() == True:
            releaseI()

        if checkJpressed() == True:
            releaseJ()

        if checkKpressed() == False:
            pressK()

        if checkLpressed() == False:
            pressL()

    # E direction
    elif (0 <= degree_theta <= 22.5 or 360 >= degree_theta >= 337.5):
        if checkIpressed() == True:
            releaseI()
        if checkJpressed() == True:
            releaseJ()
        if checkJpressed() == True:
            releaseJ()
        if checkLpressed() == False:
            pressL()

def swimming_up():
    if angle_between_14_12_24 > 150:
        if win32api.GetKeyState(0x50) >= 0:
            py.keyDown("p")
    else:
        if win32api.GetKeyState(0x50) < 0:
            py.keyUp("p")

#receive stuff
while True:
    try:
        print("turning working")

        gello = socket.recv_string()
        print("receive 1")

        hello = socket.recv_json()
        print("receive 2")

        degree_theta = hello.get("degree_theta")
        stop_turning_body = hello.get("stop_turning_body")

        angle_between_14_12_24 = hello.get("angle_between_14_12_24")
        swimming_up()
        turnbody()
        print("turning working")
    except:
        print("turning working")

        pass





