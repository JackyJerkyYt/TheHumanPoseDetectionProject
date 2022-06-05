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
socket.setsockopt_string(zmq.SUBSCRIBE, 'walking_placeblock')

#parameter for walking function

walk = 5
sprint = 6.5

right_knee_array = []
left_knee_array = []
angle_rightknee_rightankle_leftankle_array = []
angle_leftknee_leftankle_rightnkle_array = []

for i in range(4):
    left_knee_array.append(0)
    right_knee_array.append(0)
    angle_rightknee_rightankle_leftankle_array.append(0)
    angle_leftknee_leftankle_rightnkle_array.append(0)

tresholdforangle = 10




#the functions
def walking():

    global walking_stage

    # #no movement --> stop walking immeidately
    # if(
    #     ##left hip
    #         abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) < 6 and
    #         abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) < 5.5 and
    #         abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) < 5 and
    #
    #     ##left knee
    #         abs(second_frame_angle_for_left_knee - third_frame_angle_for_left_knee) < 6 and
    #         abs(third_frame_angle_for_left_knee - fourth_frame_angle_for_left_knee) < 5.5 and
    #         abs(fourth_frame_angle_for_left_knee - current_frame_angle_for_left_knee) < 5 and
    #
    #     ##right hip
    #         abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) < 6 and
    #         abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) < 5.5 and
    #         abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) < 5 and
    #
    #     ##right knee
    #         abs(second_frame_angle_for_right_knee - third_frame_angle_for_right_knee) < 6 and
    #         abs(third_frame_angle_for_right_knee - fourth_frame_angle_for_right_knee) < 5.5 and
    #         abs(fourth_frame_angle_for_right_knee - current_frame_angle_for_right_knee) < 5
    #
    #     #y coordinate of right hip not changing
    #
    #         # abs(first_frame_right_hip_y_coordinate - second_frame_right_hip_y_coordinate)*10000 < 150 and
    #         # abs(second_frame_right_hip_y_coordinate - third_frame_right_hip_y_coordinate)*10000 < 150 and
    #         # abs(third_frame_right_hip_y_coordinate - current_frame_right_hip_y_coordinate)*10000 < 150
    #
    # ):
    #     walking_stage = "not walking"
    #
    #     if win32api.GetKeyState(0x57) < 0:
    #         py.keyUp('w')
    #
    # #ANTI CHEATING MECHANISM
    #
    # if(
    #         abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) > 5 and
    #         abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) > 5 and
    #         abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) > 5 and
    #         current_frame_angle_for_left_hip > 170
    # ):
    #
    #     walking_stage = "walking"
    #
    # if (
    #         abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) > 5 and
    #         abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) > 5 and
    #         abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) > 5 and
    #         current_frame_angle_for_right_hip > 170
    # ):
    #     walking_stage = "walking"
    #
    #
    #
    # #if there is movement
    #
    # if walking_stage == "walking":
    #
    #
    #     if(
    #             abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) > 5 and
    #             abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) > 5 and
    #             abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) > 5
    #
    #     ):
    #
    #         if win32api.GetKeyState(0x57) >= 0:
    #             py.keyDown('w')
    #
    #     if (
    #             abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) > 5 and
    #             abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) > 5 and
    #             abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) > 5
    #
    #     ):
    #
    #         if win32api.GetKeyState(0x57) >= 0:
    #             py.keyDown('w')


    ################################################

    # no movement --> stop walking immeidately

    if previous_walking_stage == "walking":

        if (
                ##left hip
                abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) < 7 and
                abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) < 6 and
                abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) < 5 and

                ##left knee
                abs(second_frame_angle_for_left_knee - third_frame_angle_for_left_knee) < 7 and
                abs(third_frame_angle_for_left_knee - fourth_frame_angle_for_left_knee) < 6 and
                abs(fourth_frame_angle_for_left_knee - current_frame_angle_for_left_knee) < 5 and

                ##right hip
                abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) < 7 and
                abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) < 6 and
                abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) < 5 and

                ##right knee
                abs(second_frame_angle_for_right_knee - third_frame_angle_for_right_knee) < 7 and
                abs(third_frame_angle_for_right_knee - fourth_frame_angle_for_right_knee) < 6 and
                abs(fourth_frame_angle_for_right_knee - current_frame_angle_for_right_knee) < 5 and


                # y coordinate of right hip not changing
                abs(first_frame_right_hip_y_coordinate - second_frame_right_hip_y_coordinate)*10000 < 150 and
                abs(second_frame_right_hip_y_coordinate - third_frame_right_hip_y_coordinate)*10000 < 150 and
                abs(third_frame_right_hip_y_coordinate - current_frame_right_hip_y_coordinate)*10000 < 150

        ):
            walking_stage = "not walking"

            if win32api.GetKeyState(0x57) < 0:
                py.keyUp('w')

    else:

        if (
                ##left hip
                abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) < 6 and
                abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) < 5.5 and
                abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) < 5 and

                ##left knee
                abs(second_frame_angle_for_left_knee - third_frame_angle_for_left_knee) < 6 and
                abs(third_frame_angle_for_left_knee - fourth_frame_angle_for_left_knee) < 5.5 and
                abs(fourth_frame_angle_for_left_knee - current_frame_angle_for_left_knee) < 5 and

                ##right hip
                abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) < 6 and
                abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) < 5.5 and
                abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) < 5 and

                ##right knee
                abs(second_frame_angle_for_right_knee - third_frame_angle_for_right_knee) < 6 and
                abs(third_frame_angle_for_right_knee - fourth_frame_angle_for_right_knee) < 5.5 and
                abs(fourth_frame_angle_for_right_knee - current_frame_angle_for_right_knee) < 5


        ):
            walking_stage = "not walking"

            if win32api.GetKeyState(0x57) < 0:
                py.keyUp('w')


    # ANTI CHEATING MECHANISM

    if (
            abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) > 5 and
            abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) > 5 and
            abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) > 5 and
            current_frame_angle_for_left_hip > 170
    ):
        walking_stage = "walking"

    if (
            abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) > 5 and
            abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) > 5 and
            abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) > 5 and
            current_frame_angle_for_right_hip > 170
    ):

        walking_stage = "walking"

    # if there is movement

    if walking_stage == "walking":

        if (
                abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) > 5 and
                abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) > 5 and
                abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) > 5

        ):

            if win32api.GetKeyState(0x57) >= 0:
                py.keyDown('w')

        if (
                abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) > 5 and
                abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) > 5 and
                abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) > 5

        ):

            if win32api.GetKeyState(0x57) >= 0:
                py.keyDown('w')

def walking_with_sprinting():

    global walking_stage



    if previous_walking_stage == "walking":

        if (
                ##left hip
                abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) < 7 and
                abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) < 6 and
                abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) < 5 and

                ##left knee
                abs(second_frame_angle_for_left_knee - third_frame_angle_for_left_knee) < 7 and
                abs(third_frame_angle_for_left_knee - fourth_frame_angle_for_left_knee) < 6 and
                abs(fourth_frame_angle_for_left_knee - current_frame_angle_for_left_knee) < 5 and

                ##right hip
                abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) < 7 and
                abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) < 6 and
                abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) < 5 and

                ##right knee
                abs(second_frame_angle_for_right_knee - third_frame_angle_for_right_knee) < 7 and
                abs(third_frame_angle_for_right_knee - fourth_frame_angle_for_right_knee) < 6 and
                abs(fourth_frame_angle_for_right_knee - current_frame_angle_for_right_knee) < 5 and


                # y coordinate of right hip not changing
                abs(first_frame_right_hip_y_coordinate - second_frame_right_hip_y_coordinate)*10000 < 150 and
                abs(second_frame_right_hip_y_coordinate - third_frame_right_hip_y_coordinate)*10000 < 150 and
                abs(third_frame_right_hip_y_coordinate - current_frame_right_hip_y_coordinate)*10000 < 150

        ):
            walking_stage = "not walking"

            if win32api.GetKeyState(0x57) < 0:
                py.keyUp('w')

    else:

        if (
                ##left hip
                abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) < 6 and
                abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) < 5.5 and
                abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) < 5 and

                ##left knee
                abs(second_frame_angle_for_left_knee - third_frame_angle_for_left_knee) < 6 and
                abs(third_frame_angle_for_left_knee - fourth_frame_angle_for_left_knee) < 5.5 and
                abs(fourth_frame_angle_for_left_knee - current_frame_angle_for_left_knee) < 5 and

                ##right hip
                abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) < 6 and
                abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) < 5.5 and
                abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) < 5 and

                ##right knee
                abs(second_frame_angle_for_right_knee - third_frame_angle_for_right_knee) < 6 and
                abs(third_frame_angle_for_right_knee - fourth_frame_angle_for_right_knee) < 5.5 and
                abs(fourth_frame_angle_for_right_knee - current_frame_angle_for_right_knee) < 5


        ):
            walking_stage = "not walking"

            if win32api.GetKeyState(0x57) < 0:
                py.keyUp('w')


    # ANTI CHEATING MECHANISM

    if (
            abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) > 5 and
            abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) > 5 and
            abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) > 5 and
            current_frame_angle_for_left_hip > 170
    ):
        walking_stage = "walking"

    if (
            abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) > 5 and
            abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) > 5 and
            abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) > 5 and
            current_frame_angle_for_right_hip > 170
    ):

        walking_stage = "walking"

    # if there is movement

    if walking_stage == "walking":

        if (
               6.5 >= abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) > 5 and
                6.5 >= abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) > 5 and
                6.5 >= abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) > 5

        ):

            if win32api.GetKeyState(0x57) >= 0:
                py.keyDown('w')

            if win32api.GetKeyState(0x5A) < 0:
                py.keyUp('z')


        elif (

                abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) > 6.5 and
                abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) > 6.5 and
                abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) > 6.5

        ):
            if win32api.GetKeyState(0x57) >= 0:
                py.press('w')

            if win32api.GetKeyState(0x5A) >= 0:
                py.press('z')



        if (
                6.5 >= abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) > 5 and
                6.5 >= abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) > 5 and
                6.5 >= abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) > 5

        ):

            if win32api.GetKeyState(0x57) >= 0:
                py.keyDown('w')
            if win32api.GetKeyState(0x5A) < 0:
                py.keyUp('z')


        elif (

                abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) > 6.5 and
                abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) > 6.5 and
                abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) > 6.5

        ):
            if win32api.GetKeyState(0x57) >= 0:
                py.press('w')

            if win32api.GetKeyState(0x5A) >= 0:
                py.press('z')

def walking_final():

    global walking_stage



    if previous_walking_stage == "walking":

        if (
                ##left hip
                abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) < 7 and
                abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) < 6 and
                abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) < 5 and

                ##left knee
                abs(second_frame_angle_for_left_knee - third_frame_angle_for_left_knee) < 7 and
                abs(third_frame_angle_for_left_knee - fourth_frame_angle_for_left_knee) < 6 and
                abs(fourth_frame_angle_for_left_knee - current_frame_angle_for_left_knee) < 5 and

                ##right hip
                abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) < 7 and
                abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) < 6 and
                abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) < 5 and

                ##right knee
                abs(second_frame_angle_for_right_knee - third_frame_angle_for_right_knee) < 7 and
                abs(third_frame_angle_for_right_knee - fourth_frame_angle_for_right_knee) < 6 and
                abs(fourth_frame_angle_for_right_knee - current_frame_angle_for_right_knee) < 5 and


                # y coordinate of right hip not changing
                abs(first_frame_right_hip_y_coordinate - second_frame_right_hip_y_coordinate)*10000 < 150 and
                abs(second_frame_right_hip_y_coordinate - third_frame_right_hip_y_coordinate)*10000 < 150 and
                abs(third_frame_right_hip_y_coordinate - current_frame_right_hip_y_coordinate)*10000 < 150 and

                # y coorfinate of your knee is static

                abs(left_knee_array[3] - left_knee_array[2]) * 10000 < 120 and
                abs(left_knee_array[3] - left_knee_array[2]) * 10000 < 115 and
                abs(left_knee_array[3] - left_knee_array[2]) * 10000 < 110 and

                abs(right_knee_array[3] - right_knee_array[2]) * 10000 < 120 and
                abs(right_knee_array[3] - right_knee_array[2]) * 10000 < 115 and
                abs(right_knee_array[3] - right_knee_array[2]) * 10000 < 110


        ):
            walking_stage = "not walking"

            if win32api.GetKeyState(0x57) < 0:
                py.keyUp('w')

    else:

        if (
                ##left hip
                abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) < 6 and
                abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) < 5.5 and
                abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) < 5 and

                ##left knee
                abs(second_frame_angle_for_left_knee - third_frame_angle_for_left_knee) < 6 and
                abs(third_frame_angle_for_left_knee - fourth_frame_angle_for_left_knee) < 5.5 and
                abs(fourth_frame_angle_for_left_knee - current_frame_angle_for_left_knee) < 5 and

                ##right hip
                abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) < 6 and
                abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) < 5.5 and
                abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) < 5 and

                ##right knee
                abs(second_frame_angle_for_right_knee - third_frame_angle_for_right_knee) < 6 and
                abs(third_frame_angle_for_right_knee - fourth_frame_angle_for_right_knee) < 5.5 and
                abs(fourth_frame_angle_for_right_knee - current_frame_angle_for_right_knee) < 5 and

                abs(left_knee_array[3] - left_knee_array[2]) * 10000 < 120 and
                abs(left_knee_array[3] - left_knee_array[2]) * 10000 < 115 and
                abs(left_knee_array[3] - left_knee_array[2]) * 10000 < 110 and

                abs(right_knee_array[3] - right_knee_array[2]) * 10000 < 120 and
                abs(right_knee_array[3] - right_knee_array[2]) * 10000 < 115 and
                abs(right_knee_array[3] - right_knee_array[2]) * 10000 < 110


        ):
            walking_stage = "not walking"

            if win32api.GetKeyState(0x57) < 0:
                py.keyUp('w')


    # ANTI CHEATING MECHANISM

    if (
            (abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) > 5 and
            abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) > 5 and
            abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) > 5 and
            current_frame_angle_for_left_hip > 170)

            or (

            abs(angle_rightknee_rightankle_leftankle_array[3] - angle_rightknee_rightankle_leftankle_array[2])>tresholdforangle and
            abs(angle_rightknee_rightankle_leftankle_array[2] - angle_rightknee_rightankle_leftankle_array[1])>tresholdforangle and
            abs(angle_rightknee_rightankle_leftankle_array[1] - angle_rightknee_rightankle_leftankle_array[0])>tresholdforangle and
            ( angle_rightknee_rightankle_leftankle_array[3] > 78)

            )


    ):
        walking_stage = "walking"

        if win32api.GetKeyState(0x57) >= 0:
            py.keyDown('w')

    if (
            (abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) > 5 and
            abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) > 5 and
            abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) > 5 and
            current_frame_angle_for_right_hip > 170)

            or (

            abs(angle_leftknee_leftankle_rightnkle_array[3] - angle_leftknee_leftankle_rightnkle_array[
                2]) > tresholdforangle and
            abs(angle_leftknee_leftankle_rightnkle_array[2] - angle_leftknee_leftankle_rightnkle_array[
                1]) > tresholdforangle and
            abs(angle_leftknee_leftankle_rightnkle_array[1] - angle_leftknee_leftankle_rightnkle_array[
                0]) > tresholdforangle and
            ( angle_leftknee_leftankle_rightnkle_array[3] > 78)

            )

    ):

        walking_stage = "walking"

        if win32api.GetKeyState(0x57) >= 0:
            py.keyDown('w')

    # if there is movement

    if walking_stage == "walking":

        if (
                abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip) > 5 and
                abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip) > 5 and
                abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip) > 5

        ):

            if win32api.GetKeyState(0x57) >= 0:
                py.keyDown('w')

        if (
                abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip) > 5 and
                abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip) > 5 and
                abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip) > 5

        ):

            if win32api.GetKeyState(0x57) >= 0:
                py.keyDown('w')


# def placeblock1():
#     global place_block_stage
#     global previous_place_block_stage
#
#     if angle_between_rightwrist_rightelbow_leftelbow < 25:
#         place_block_stage = "ready"
#
#     if angle_between_rightwrist_rightelbow_leftelbow > 70:
#         place_block_stage = "placed"
#
#     if place_block_stage == "placed" and previous_place_block_stage == "ready":
#         py.click(button="right", duration=1)

def placeblockV1():
    if current_frame_right_hand_x_coordinate > current_frame_right_shoulder_x_coordinate:
        place_block_stage = "ready"

    if(
            ((first_frame_right_hand_x_coordinate - second_frame_right_hand_x_coordinate) > 0.20) and
            ((second_frame_right_hand_x_coordinate - third_frame_right_hand_x_coordinate) > 0.20) and
            ((third_frame_right_hand_x_coordinate - current_frame_right_hand_x_coordinate) > 0.20) and
            place_block_stage == "ready"
    ):
        place_block_stage = "placed"
        py.click(button="right", duration=1)


    #this version will have the problem where it will place block mulitple times in one swing as it detects your right hand is till in the your body range

def placeblockV2():
    global place_block_stage

    i = 0

    if current_frame_right_hand_x_coordinate < current_frame_right_shoulder_x_coordinate:

        place_block_stage = "outside"

    if place_block_stage == "outside" and (current_frame_right_hand_x_coordinate > current_frame_right_shoulder_x_coordinate):

        place_block_stage = "ready"

    if (
            ((first_frame_right_hand_x_coordinate - second_frame_right_hand_x_coordinate)/shoulder_length > 0) and
            ((second_frame_right_hand_x_coordinate - third_frame_right_hand_x_coordinate)/shoulder_length > 0) and
            ((third_frame_right_hand_x_coordinate - current_frame_right_hand_x_coordinate)/shoulder_length > 0.016) and
            place_block_stage == "ready"
    ):
        place_block_stage = "placed"
        print(i,"placed","third current",(third_frame_right_hand_x_coordinate - current_frame_right_hand_x_coordinate)/shoulder_length, "second_third", (second_frame_right_hand_x_coordinate - third_frame_right_hand_x_coordinate)/shoulder_length)
        # py.click(button="right", duration=1)
        i = i + 1

def placeblockV3():

    if current_frame_right_hand_x_coordinate > current_frame_right_shoulder_x_coordinate and not(((first_frame_right_hand_x_coordinate - second_frame_right_hand_x_coordinate) > 0.20) and
            ((second_frame_right_hand_x_coordinate - third_frame_right_hand_x_coordinate) > 0.20) and
            ((third_frame_right_hand_x_coordinate - current_frame_right_hand_x_coordinate) > 0.20)):
        place_block_stage = "ready"

    if(
            ((first_frame_right_hand_x_coordinate - second_frame_right_hand_x_coordinate) > 0.20) and
            ((second_frame_right_hand_x_coordinate - third_frame_right_hand_x_coordinate) > 0.20) and
            ((third_frame_right_hand_x_coordinate - current_frame_right_hand_x_coordinate) > 0.20) and
            place_block_stage == "ready"
    ):
        place_block_stage = "placed"
        py.click(button="right", duration=1)


#intialise something

#Right Hip:

first_frame_angle_for_right_hip = 0
second_frame_angle_for_right_hip = 0
third_frame_angle_for_right_hip = 0
fourth_frame_angle_for_right_hip = 0
current_frame_angle_for_right_hip = 0

#Left hip:

first_frame_angle_for_left_hip = 0
second_frame_angle_for_left_hip = 0
third_frame_angle_for_left_hip = 0
fourth_frame_angle_for_left_hip = 0
current_frame_angle_for_left_hip = 0

#Left knee:

first_frame_angle_for_left_knee = 0
second_frame_angle_for_left_knee = 0
third_frame_angle_for_left_knee = 0
fourth_frame_angle_for_left_knee = 0
current_frame_angle_for_left_knee = 0

#Right knee:

first_frame_angle_for_right_knee = 0
second_frame_angle_for_right_knee = 0
third_frame_angle_for_right_knee = 0
fourth_frame_angle_for_right_knee = 0
current_frame_angle_for_right_knee = 0

#Y corrdinate for right hip

first_frame_right_hip_y_coordinate = 0
second_frame_right_hip_y_coordinate = 0
third_frame_right_hip_y_coordinate = 0
current_frame_right_hip_y_coordinate = 0






#x coordinate of right hand

first_frame_right_hand_x_coordinate = 0
second_frame_right_hand_x_coordinate = 0
third_frame_right_hand_x_coordinate = 0
current_frame_right_hand_x_coordinate = 0

#x coordinate of right shoulder

current_frame_right_shoulder_x_coordinate = 0

#ycoordinate for knee

current_frame_right_knee_y_coordinate = 0
current_frame_left_knee_y_coordinate = 0

#angle for knee and ankle

current_frame_angle_rightknee_rightankle_leftankle = 0

current_frame_angle_leftknee_lefttankle_rightankle = 0
#Walking stage:

walking_stage = ""
previous_walking_stage = ""


#initial varaible
place_block_stage = ""
previous_place_block_stage = ""
testing = 2

shoulder_length = 0

print("hello")
execute_placeblock = 0

#receive stuff
while True:
    try:

        socket.connect("tcp://localhost:5555")
        print("connected")

        gello = socket.recv_string()
        hello = socket.recv_json()


        current_frame_angle_for_right_hip = hello.get("current_frame_angle_for_right_hip")
        current_frame_angle_for_left_hip = hello.get("current_frame_angle_for_left_hip")
        current_frame_angle_for_left_knee = hello.get("current_frame_angle_for_left_knee")
        current_frame_angle_for_right_knee = hello.get("current_frame_angle_for_right_knee")
        current_frame_right_hip_y_coordinate = hello.get("current_frame_right_hip_y_coordinate")
        current_frame_right_knee_y_coordinate = hello.get("right_knee_y")
        current_frame_left_knee_y_coordinate = hello.get("left_knee_y")
        current_frame_angle_rightknee_rightankle_leftankle = hello.get("angle_rightknee_rightankle_leftankle")
        current_frame_angle_leftknee_lefttankle_rightankle = hello.get("angle_leftknee_lefttankle_rightankle")

        #walking

        # current_frame_angle_for_right_hip = data[5]
        #
        # current_frame_angle_for_left_hip = data[4]
        #
        # current_frame_angle_for_left_knee = data[6]
        #
        # current_frame_angle_for_right_knee = data[7]
        #
        # current_frame_right_hip_y_coordinate = data[0]

        #placeblock

        # execute_placeblock = data[9]

        #execute the functions

        angle_leftknee_leftankle_rightnkle_array.append(current_frame_angle_leftknee_lefttankle_rightankle)
        angle_leftknee_leftankle_rightnkle_array.pop(0)

        angle_rightknee_rightankle_leftankle_array.append(current_frame_angle_rightknee_rightankle_leftankle)
        angle_rightknee_rightankle_leftankle_array.pop(0)

        right_knee_array.append(current_frame_right_knee_y_coordinate)
        right_knee_array.pop(0)

        left_knee_array.append(current_frame_left_knee_y_coordinate)
        left_knee_array.pop(0)

        print((

            abs(angle_rightknee_rightankle_leftankle_array[3] - angle_rightknee_rightankle_leftankle_array[2])>tresholdforangle and
            abs(angle_rightknee_rightankle_leftankle_array[2] - angle_rightknee_rightankle_leftankle_array[1])>tresholdforangle and
            abs(angle_rightknee_rightankle_leftankle_array[1] - angle_rightknee_rightankle_leftankle_array[0])>tresholdforangle and
            (angle_rightknee_rightankle_leftankle_array[3] > 78)

            ))

        walking_final()

        # print(angle_leftknee_leftankle_rightnkle_array)




        # if(execute_placeblock == 1):
        #     py.click(button="right", duration=1)
        # if place_block_stage == "placed":
        #     print(place_block_stage)
        # # print(((first_frame_right_hand_x_coordinate - second_frame_right_hand_x_coordinate) > 0.1) and
        # #     ((second_frame_right_hand_x_coordinate - third_frame_right_hand_x_coordinate) < 0.1) and
        # #     ((third_frame_right_hand_x_coordinate - current_frame_right_hand_x_coordinate) > 0.1) )
        # if((-current_frame_right_hand_x_coordinate+third_frame_right_hand_x_coordinate)*100 >0 or (second_frame_right_hand_x_coordinate - third_frame_right_hand_x_coordinate)*100 >0):
        #     print(-current_frame_right_hand_x_coordinate*100 + third_frame_right_hand_x_coordinate*100,(second_frame_right_hand_x_coordinate - third_frame_right_hand_x_coordinate)*-1*100)
        # print(current_frame_right_hand_x_coordinate)
        # print(f'current-thirdframe: {round((current_frame_right_hip_y_coordinate - third_frame_right_hip_y_coordinate)*10000)}, third-secondframe: {round((third_frame_right_hip_y_coordinate-second_frame_right_hip_y_coordinate)*10000)}, second-firstframe: {round((second_frame_right_hip_y_coordinate-first_frame_right_hip_y_coordinate)*10000)}')
        # print(walking_stage)

        # if (abs(second_frame_angle_for_left_knee - third_frame_angle_for_left_knee)>=testing):
        #     print("second third frame left knee")
        # if(abs(third_frame_angle_for_left_knee - fourth_frame_angle_for_left_knee)>=testing):
        #     print("third fourth frame left knee")
        # if(abs(fourth_frame_angle_for_left_knee - current_frame_angle_for_left_knee)>=testing):
        #     print("fourth current frame left knee")
        #
        #
        # if (abs(second_frame_angle_for_left_hip - third_frame_angle_for_left_hip)>=testing):
        #     print("second third frame left hip")
        # if(abs(third_frame_angle_for_left_hip - fourth_frame_angle_for_left_hip)>=testing):
        #     print("third fourth frame left hip")
        # if(abs(fourth_frame_angle_for_left_hip - current_frame_angle_for_left_hip)>=testing):
        #     print("fourth current frame left hip")
        #
        #
        # if (abs(second_frame_angle_for_right_knee - third_frame_angle_for_right_knee)>=testing):
        #     print("second third frame right knee")
        # if(abs(third_frame_angle_for_right_knee - fourth_frame_angle_for_right_knee)>=testing):
        #     print("third fourth frame right knee")
        # if(abs(fourth_frame_angle_for_right_knee - current_frame_angle_for_right_knee)>=testing):
        #     print("fourth current frame right knee")
        #
        #
        # if (abs(second_frame_angle_for_right_hip - third_frame_angle_for_right_hip)>=testing):
        #     print("second third frame right hip")
        # if(abs(third_frame_angle_for_right_hip - fourth_frame_angle_for_right_hip)>=testing):
        #     print("third fourth frame right hip")
        # if(abs(fourth_frame_angle_for_right_hip - current_frame_angle_for_right_hip)>=testing):
        #     print("fourth current frame right hip")




        #Updating variables

        #walking

        # Right Hip:

        first_frame_angle_for_right_hip = second_frame_angle_for_right_hip
        second_frame_angle_for_right_hip = third_frame_angle_for_right_hip
        third_frame_angle_for_right_hip = fourth_frame_angle_for_right_hip
        fourth_frame_angle_for_right_hip = current_frame_angle_for_right_hip

        # Left hip:

        first_frame_angle_for_left_hip = second_frame_angle_for_left_hip
        second_frame_angle_for_left_hip = third_frame_angle_for_left_hip
        third_frame_angle_for_left_hip = fourth_frame_angle_for_left_hip
        fourth_frame_angle_for_left_hip = current_frame_angle_for_left_hip

        # Left knee:

        first_frame_angle_for_left_knee = second_frame_angle_for_left_knee
        second_frame_angle_for_left_knee = third_frame_angle_for_left_knee
        third_frame_angle_for_left_knee = fourth_frame_angle_for_left_knee
        fourth_frame_angle_for_left_knee = current_frame_angle_for_left_knee

        # Right knee:

        first_frame_angle_for_right_knee = second_frame_angle_for_right_knee
        second_frame_angle_for_right_knee = third_frame_angle_for_right_knee
        third_frame_angle_for_right_knee = fourth_frame_angle_for_right_knee
        fourth_frame_angle_for_right_knee = current_frame_angle_for_right_knee

        #placeblock stage

        previous_place_block_stage = place_block_stage

        #Walking stage

        previous_walking_stage = walking_stage

        #ycoordinate for right hip

        first_frame_right_hip_y_coordinate = second_frame_right_hip_y_coordinate
        second_frame_right_hip_y_coordinate = third_frame_right_hip_y_coordinate
        third_frame_right_hip_y_coordinate = current_frame_right_hip_y_coordinate


        #x coordinate for right hand for placeblock

        first_frame_right_hand_x_coordinate = second_frame_right_hand_x_coordinate
        second_frame_right_hand_x_coordinate = third_frame_right_hand_x_coordinate
        third_frame_right_hand_x_coordinate = current_frame_right_hand_x_coordinate

        socket.disconnect("tcp://localhost:5555")



    except:
        print("hello")
        pass