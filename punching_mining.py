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
#jumping_punching_mining.py
#Set up subscriber
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")
socket.setsockopt_string(zmq.SUBSCRIBE, 'jumping_punching_mining')

#functions
def jumping():

    py.press('p', interval=0.2)

def punching():
    global stage

    if angle_between_14_12_24 > 40 and stage == "Down":
        stage = "up"
        py.click()

    if angle_between_14_12_24 < 19 and stage == "up":
        stage = "Down"

def holding_right_key():

    if angle_between_16_14_12<160:

        if (angle_between_14_12_24 < 30 and

        angle_between_16_14_12 < 80 and

        abs(angle_between_16_14_12-fifth_frame_angle_between_16_14_12) > 8 and

        abs(fifth_frame_angle_between_16_14_12 - fourth_frame_angle_between_16_14_12) > 8 and

        abs(fourth_frame_angle_between_16_14_12 - third_frame_angle_between_16_14_12) > 8 and

        abs(third_frame_angle_between_16_14_12 - second_frame_angle_between_16_14_12) > 8 and

        abs(second_frame_angle_between_16_14_12 - first_frame_angle_between_16_14_12) > 8):

            if win32api.GetKeyState(0x01) >= 0:
                py.mouseDown()

        if (angle_between_14_12_24 <30 and

        abs(angle_between_16_14_12-third_frame_angle_between_16_14_12) < 5 and

        abs(third_frame_angle_between_16_14_12 - second_frame_angle_between_16_14_12) < 6 and

        abs(second_frame_angle_between_16_14_12 - first_frame_angle_between_16_14_12) < 8):

            if win32api.GetKeyState(0x01) < 0:
                py.mouseUp()

    elif win32api.GetKeyState(0x01) < 0:
        py.mouseUp()

#initial varaible

previous_y_coordinate_for_right_hip = 0

stage = "Down"

first_frame_angle_between_16_14_12 = 0
second_frame_angle_between_16_14_12 = 0
third_frame_angle_between_16_14_12 = 0
fourth_frame_angle_between_16_14_12 = 0
fifth_frame_angle_between_16_14_12 = 0
sixth_frame_angle_between_16_14_12 = 0
seventh_frame_angle_between_16_14_12 = 0
eighth_frame_angle_between_16_14_12 = 0


angle_between_16_14_12 = 0

execute_jumping = 0

#receive stuff
while True:
    try:

        gello = socket.recv_string()
        hello = socket.recv_json()
        print("hello")
        angle_between_16_14_12 = hello.get("angle_between_16_14_12")
        angle_between_14_12_24 = hello.get("angle_between_14_12_24")

        #Functions:

        punching()

        holding_right_key()

        #updating variables

        first_frame_angle_between_16_14_12 = second_frame_angle_between_16_14_12

        second_frame_angle_between_16_14_12 = third_frame_angle_between_16_14_12

        third_frame_angle_between_16_14_12 = fourth_frame_angle_between_16_14_12

        fourth_frame_angle_between_16_14_12 = fifth_frame_angle_between_16_14_12

        fifth_frame_angle_between_16_14_12 = angle_between_16_14_12

    except:
        pass