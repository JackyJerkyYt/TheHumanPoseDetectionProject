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

#Set up Publisher
context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

shouldIjump = "no"

classNames = []
classFile = 'names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

def calculateangle(a,b,c):
    a = np.array(a) #First
    b = np.array(b) #Second
    c = np.array(c) #Third

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

def new_calculate_angle():
    xdistance = -1 * left_hand_x + left_elbow_x
    ydistance = -1 * left_hand_y + left_elbow_y
    theta = np.arctan2(ydistance,xdistance)
    if theta>0:
        theta = theta
    else:
        theta = 2 * 3.141596 + theta
    return theta * 180 / 3.141596


def eating():
    if abs(left_hand_x - mouth_x) < 0.03 and abs(left_hand_y - mouth_y) < 0.03:

        if win32api.GetKeyState(0x02) >= 0:
            py.mouseDown(button="right")
        # else:


    else:

        if win32api.GetKeyState(0x02) < 0:
            py.mouseUp(button="right")
        # else:

start = 0
end = 0

#Open cv
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

thres = 0.4#test_object_detection.py # Threshold to detect object
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

#backpack mode

inventory_mode = "close"
previous_inventory_mode = "close"

#choosing mode

choosing_mode = ""
previous_choosing_mode = "close"
is_choosing_mode_open_now = False
current_is_it_in_ready_mode_for_choosing_mode = False
first_is_it_in_ready_mode_for_choosing_mode = False
second_is_it_in_ready_mode_for_choosing_mode = False
third_is_it_in_ready_mode_for_choosing_mode = False
fourth_is_it_in_ready_mode_for_choosing_mode = False
fifth_is_it_in_ready_mode_for_choosing_mode = False
sixth_is_it_in_ready_mode_for_choosing_mode = False
seventh_is_it_in_ready_mode_for_choosing_mode = False
eighth_is_it_in_ready_mode_for_choosing_mode = False
ninth_is_it_in_ready_mode_for_choosing_mode = False


#turnbody sudden change variable

first_frame_radius = 0
second_frame_radius = 0
third_frame_radius = 0
current_frame_radius = 0
shoulder_length = 0

hip_length = 0

length_of_right_hand_in_the_hip = 0

placeblock_x_coordinate_treshold = 0

current_whether_the_right_hand_meet_the_placeblock_x_coordinate_treshold = 0

current_placeblock_x = 0
first_placeblock_x = 0
second_placeblock_x = 0
third_placeblock_x = 0
fourth_placeblock_x = 0
fifth_placeblock_x = 0
sixth_placeblock_x = 0
seventh_placeblock_x = 0
eigth_placeblock_x = 0
ninth_placeblock_x = 0
tenth_placeblock_x = 0
eleventh_placeblock_x = 0

execute_placeblock = 0
execute_jumping = 0

current_placeblock_stage = "nothing"
previous_placeblock_stage = "nothing"

right_hip_y_tres_for_jumping = 0

hip_to_shoulder_tres = 0


number_of_frames_for_jumping = 6

right_shoulder_y_coordinate_array = []
right_hip_y_coordinate_array = []
left_shoulder_y_coordinate_array = []
left_hip_y_coordinate_array = []
length_of_shoulder_array = []
left_feet_y_coordinate_array = []
right_feet_y_coordinate_array = []

jumping_stage = "nothing"

storing_left_y_coordinate = 0
storing_right_y_coordinate = 0



for i in range(number_of_frames_for_jumping):
    right_shoulder_y_coordinate_array.append(0)
    right_hip_y_coordinate_array.append(0)
    left_shoulder_y_coordinate_array.append(0)
    left_hip_y_coordinate_array.append(0)

for i in range(3):
    length_of_shoulder_array.append(0)

for i in range(2):
    left_feet_y_coordinate_array.append(0)
    right_feet_y_coordinate_array.append(0)


condition_for_right_shoulder = True
condition_for_right_hip = True
condition_for_left_shoulder = True
condition_for_left_hip = True
it_shoulder_length_doesn_move = True
left_feet_doesnt_move_up_down = True
right_feet_doesnt_move_up_down = True

i = 0

with mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6) as pose:
    while cap.isOpened():

        ret, frame = cap.read()
        # Recolor Image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # make Detection
        results = pose.process(image)

        # Recolor back to BGR

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # extract Landmarks

        try:

            landmarks = results.pose_landmarks.landmark

            #back pack detection:

            #detect that the feet are gone

            # if (landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].visibility < 0.5 or landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].visibility < 0.5):
            #     classIds, confs, bbox = net.detect(image, confThreshold=thres)
            #     # print(classIds, bbox)
            #         #test_object_detection.py
            #     if len(classIds) != 0:
            #         for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            #             cv2.rectangle(image, box, color=(0, 255, 0), thickness=2)
            #             cv2.putText(image, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
            #                         cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            #             cv2.putText(image, str(round(confidence * 100, 2)), (box[0] + 200, box[1] + 30),
            #                         cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
            #
            #             if(classNames[classId - 1].upper() == "BACKPACK"):
            #                 inventory_mode = "open"
            #                 if(previous_inventory_mode =="close" and inventory_mode == "open"):
            #                     print("press e to open")
            #                     py.press("e")
            #
            #                 previous_inventory_mode = inventory_mode
            #                 break
            # else:
            #     if(previous_inventory_mode == "open"):
            #         print("press e to close")
            #         inventory_mode = "close"
            #         py.press("e")
            #         previous_inventory_mode = inventory_mode

            if (landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].visibility < 0.5 and (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y > landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y or landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y > landmarks[mp_pose.PoseLandmark.Left_KNEE.value].y) ):
                inventory_mode = "open"
                if(previous_inventory_mode =="close" and inventory_mode == "open"):
                    # py.press("e")
                    pass
                previous_inventory_mode = inventory_mode
            else:
                if(previous_inventory_mode == "open"):
                    inventory_mode = "close"
                    # py.press("e")
                    previous_inventory_mode = inventory_mode

            # Get Coordinates

            right_shoulder_12 = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

            left_shoulder_11 = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]


            left_shoulder_x = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x

            left_shoulder_y = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y

            right_elbow_14 = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

            left_elbow_13 = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]

            right_wrist_16 = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            left_wrist_15 = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            right_hip_24 = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                            landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]

            left_hip_23 = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                           landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]

            left_knee_25 = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]

            right_knee_26 = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                             landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]

            left_ankle_27 = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                             landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]

            right_ankle_28 = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                              landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            left_hand = [landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y]

            right_hand = [landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y]

            left_feet = [landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]

            right_feet = [landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]

            left_feet_y = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y

            right_feet_y = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y


            right_hip_y_coordinate = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y

            right_hip_x_coordinate = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x

            left_hip_y_coordinate = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y

            left_hip_x_coordinate = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x

            left_hand_x = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x

            left_hand_y = landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y

            left_hand_z = landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].z

            left_elbow_x = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x

            left_elbow_y = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y

            right_hip_y = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y

            right_shoulder_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y

            right_shoulder_x = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x

            right_elbow_y = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y

            mouth_x = landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].x

            mouth_y = landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value].x

            right_hand_y = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y

            right_hand_x = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x

            right_index_x = landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].x

            left_index_x = landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x

            left_knee_y = landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y

            right_knee_y = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y

            left_ankle_y = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y

            right_ankle_y = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y


            # Calculate Angle

            angle_between_16_14_12 = calculateangle(right_wrist_16, right_elbow_14, right_shoulder_12)
            angle_between_15_13_11 = calculateangle(left_wrist_15, left_elbow_13, left_shoulder_11)
            angle_between_14_12_24 = calculateangle(right_elbow_14, right_shoulder_12, right_hip_24)
            angle_between_11_23_25 = calculateangle(left_shoulder_11, left_hip_23, left_knee_25)
            angle_between_12_24_26 = calculateangle(right_shoulder_12, right_hip_24, right_knee_26)
            angle_between_23_25_27_left = calculateangle(left_hip_23, left_knee_25, left_ankle_27)
            angle_between_24_26_28_right = calculateangle(right_hip_24, right_knee_26, right_ankle_28)

            angle_between_leftshoulder_leftelbow_leftwrist = calculateangle(left_shoulder_11, left_elbow_13,
                                                                            left_wrist_15)

            angle_between_rightshoulder_leftelbow_leftwrist = calculateangle(right_shoulder_12, left_elbow_13,
                                                                             left_wrist_15)

            angle_between_rightelbow_leftelbow_leftshoulder = calculateangle(right_elbow_14, left_elbow_13,
                                                                             right_shoulder_12)

            angle_between_rightwrist_rightelbow_leftelbow = calculateangle(right_wrist_16, right_elbow_14, left_elbow_13)


            degree_theta = new_calculate_angle()

            shoulder_length = math.sqrt((left_shoulder_x - right_shoulder_x)*(left_shoulder_x - right_shoulder_x) + (left_shoulder_y - right_shoulder_y)*(left_shoulder_y - right_shoulder_y))

            angle_rightknee_rightankle_leftankle = calculateangle(right_knee_26, right_ankle_28, left_ankle_27)

            angle_leftknee_lefttankle_rightankle = calculateangle(left_knee_25, left_ankle_27, right_ankle_28)


            #
            # print("{{", "left knee: ", angle_between_23_25_27_left, "right knee: ", angle_between_24_26_28_right)
            # print("left hip: ", angle_between_11_23_25, "right hip: ", angle_between_12_24_26, "}}")
            # print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")



            ##choosing state

            if(angle_between_16_14_12>170 and angle_between_14_12_24 < 18):
                current_is_it_in_ready_mode_for_choosing_mode = True
            else:
                current_is_it_in_ready_mode_for_choosing_mode = False

            if(first_is_it_in_ready_mode_for_choosing_mode == True and current_is_it_in_ready_mode_for_choosing_mode == True):
                choosing_mode = "open"
                if (previous_choosing_mode == "close" and choosing_mode == "open"):
                    is_choosing_mode_open_now = True
                previous_choosing_mode = choosing_mode

            else:
                if (previous_choosing_mode == "open"):
                    choosing_mode = "close"
                    previous_choosing_mode = choosing_mode
                    is_choosing_mode_open_now = False

            # print("choosing_mode:",is_choosing_mode_open_now,"|| inventory mode:", inventory_mode)

            first_is_it_in_ready_mode_for_choosing_mode = second_is_it_in_ready_mode_for_choosing_mode
            second_is_it_in_ready_mode_for_choosing_mode = third_is_it_in_ready_mode_for_choosing_mode
            third_is_it_in_ready_mode_for_choosing_mode = fourth_is_it_in_ready_mode_for_choosing_mode
            fourth_is_it_in_ready_mode_for_choosing_mode = fifth_is_it_in_ready_mode_for_choosing_mode
            fifth_is_it_in_ready_mode_for_choosing_mode = sixth_is_it_in_ready_mode_for_choosing_mode
            sixth_is_it_in_ready_mode_for_choosing_mode = seventh_is_it_in_ready_mode_for_choosing_mode
            seventh_is_it_in_ready_mode_for_choosing_mode = eighth_is_it_in_ready_mode_for_choosing_mode
            eighth_is_it_in_ready_mode_for_choosing_mode = ninth_is_it_in_ready_mode_for_choosing_mode
            ninth_is_it_in_ready_mode_for_choosing_mode = current_is_it_in_ready_mode_for_choosing_mode

            if(is_choosing_mode_open_now == True):
                socket.send_pyobj([(degree_theta + 10000)])
                print(degree_theta)

            if(is_choosing_mode_open_now == False):
                 # turning body


                tres = math.sqrt((left_elbow_x - left_shoulder_x)*(left_elbow_x - left_shoulder_x) + (left_elbow_y - left_shoulder_y)*(left_elbow_y - left_shoulder_y))

                if((math.sqrt((left_hand_x - left_elbow_x)*(left_hand_x - left_elbow_x)+(left_hand_y - left_elbow_y)*(left_hand_y - left_elbow_y))) < tres/2.1):
                    stop_turning_body = 1
                else:
                    stop_turning_body = 0

                #eating

                # eating()

                #placeblock

                mid_hip_length = 0.5 * abs(right_shoulder_x - left_shoulder_x)

                length_of_right_hand_in_the_hip = right_index_x - right_shoulder_x

                placeblock_x_coordinate_treshold = mid_hip_length + right_hip_x_coordinate

                if(right_index_x >= placeblock_x_coordinate_treshold):
                    current_placeblock_x = True
                else:
                    current_placeblock_x = False

                if(right_index_x > right_shoulder_x):
                    current_placeblock_stage = "inside"
                else:
                    current_placeblock_stage = "outside"

                if(current_placeblock_stage == "outside" and previous_placeblock_stage == "inside"):

                    if(ninth_placeblock_x == True):
                        execute_placeblock = 1
                        print("placed")

                    if (execute_placeblock == 1):
                        py.click(button="right", duration=0.2)

                first_placeblock_x = second_placeblock_x
                second_placeblock_x = third_placeblock_x
                third_placeblock_x = fourth_placeblock_x
                fourth_placeblock_x = fifth_placeblock_x
                fifth_placeblock_x = sixth_placeblock_x
                sixth_placeblock_x = seventh_placeblock_x
                seventh_placeblock_x = eigth_placeblock_x
                eigth_placeblock_x = ninth_placeblock_x
                ninth_placeblock_x = tenth_placeblock_x
                tenth_placeblock_x = eleventh_placeblock_x
                eleventh_placeblock_x = current_placeblock_x

                previous_placeblock_stage = current_placeblock_stage

                #jumping
                # right_hip_y_coordinate_array.append(right_hip_y)
                # right_hip_y_coordinate_array.pop(0)
                #
                # right_hip_y_coordinate_derivative_array[0] = right_hip_y_coordinate_array[1] - right_hip_y_coordinate_derivative_array[0]
                # right_hip_y_coordinate_derivative_array[1] = right_hip_y_coordinate_array[2] - right_hip_y_coordinate_derivative_array[1]
                # right_hip_y_coordinate_derivative_array[2] = right_hip_y_coordinate_array[3] - right_hip_y_coordinate_derivative_array[2]
                # right_hip_y_coordinate_derivative_array[3] = right_hip_y_coordinate_array[4] - right_hip_y_coordinate_derivative_array[3]
                #
                # right_hip_y_coordinate_second_derivative_array[0] = right_hip_y_coordinate_array[1] - right_hip_y_coordinate_second_derivative_array[0]
                # right_hip_y_coordinate_second_derivative_array[1] = right_hip_y_coordinate_array[2] - right_hip_y_coordinate_second_derivative_array[1]
                # right_hip_y_coordinate_second_derivative_array[2] = right_hip_y_coordinate_array[3] -  right_hip_y_coordinate_second_derivative_array[2]

                left_hip_y_coordinate_array.append(left_hip_y_coordinate)
                left_hip_y_coordinate_array.pop(0)

                left_shoulder_y_coordinate_array.append(left_shoulder_y)
                left_shoulder_y_coordinate_array.pop(0)

                right_hip_y_coordinate_array.append(right_hip_y)
                right_hip_y_coordinate_array.pop(0)

                right_shoulder_y_coordinate_array.append(right_shoulder_y)
                right_shoulder_y_coordinate_array.pop(0)

                length_of_shoulder_array.append(shoulder_length)
                length_of_shoulder_array.pop(0)

                left_feet_y_coordinate_array.append(left_feet_y)
                left_feet_y_coordinate_array.pop(0)

                right_feet_y_coordinate_array.append(right_feet_y)
                right_feet_y_coordinate_array.pop(0)


                for index, element in enumerate(right_hip_y_coordinate_array):
                    if (index >= 1):
                        if right_hip_y_coordinate_array[index] < right_hip_y_coordinate_array[index - 1]:
                            condition_for_right_hip = False

                for index, element in enumerate(right_shoulder_y_coordinate_array):
                    if (index >= 1):
                        if right_shoulder_y_coordinate_array[index] < right_shoulder_y_coordinate_array[index - 1]:
                            condition_for_right_shoulder = False

                for index, element in enumerate(left_hip_y_coordinate_array):
                    if (index >= 1):
                        if left_hip_y_coordinate_array[index] < left_hip_y_coordinate_array[index - 1]:
                            condition_for_left_hip = False

                for index, element in enumerate(left_shoulder_y_coordinate_array):
                    if (index >= 1):
                        if left_shoulder_y_coordinate_array[index] < left_shoulder_y_coordinate_array[index - 1]:
                            condition_for_left_shoulder = False


                if(abs(length_of_shoulder_array[len(length_of_shoulder_array) - 1] - length_of_shoulder_array[0]) > 0.022):
                    it_shoulder_length_doesn_move = False

                if(abs(left_feet_y_coordinate_array[1]-left_feet_y_coordinate_array[0]) > 0.014):
                    left_feet_doesnt_move_up_down = False

                if(abs(right_feet_y_coordinate_array[1] - right_feet_y_coordinate_array[0]) > 0.014):
                    right_feet_doesnt_move_up_down = False

                shouldIjump = "no"


                if(condition_for_left_shoulder and condition_for_left_hip and condition_for_right_hip and condition_for_right_shoulder and it_shoulder_length_doesn_move and left_feet_doesnt_move_up_down and right_feet_doesnt_move_up_down):
                    print(i, "squated")
                    storing_left_y_coordinate = left_feet_y
                    storing_right_y_coordinate = right_feet_y
                    jumping_stage = "squating"

                if(angle_rightknee_rightankle_leftankle < 58 or angle_leftknee_lefttankle_rightankle < 58):
                    jumping_stage = "jumping"
                    print("cancelled")

                if(jumping_stage == "squating"):
                    if(storing_left_y_coordinate - left_feet_y > 0.015 and storing_right_y_coordinate - right_feet_y > 0.015):
                        py.press('p')
                        shouldIjump = "yes"
                        print(i, "jumped")
                        jumping_stage = "jumping"

                # if(jumping_stage == "squating"):
                #     storing_left_y_coordinate = left_feet_y
                #     storing_right_y_coordinate = right_feet_y


                condition_for_right_shoulder = True
                condition_for_right_hip = True
                condition_for_left_hip = True
                condition_for_left_shoulder = True
                it_shoulder_length_doesn_move = True
                left_feet_doesnt_move_up_down = True
                right_feet_doesnt_move_up_down = True

                # socket.send_pyobj([right_hip_y_coordinate,  #0 #
                #                     stop_turning_body,  #1#
                #                    angle_between_16_14_12,  #2#
                #                    angle_between_14_12_24,  #3#
                #                    angle_between_11_23_25,  #4#
                #                    angle_between_12_24_26,  #5#
                #                    angle_between_23_25_27_left,  #6#
                #                    angle_between_24_26_28_right,  #7#
                #                    degree_theta, #8
                #                    # execute_placeblock, #9
                #                    # execute_jumping
                #                     ])

                socket.send_string("jumping_punching_mining", flags=zmq.SNDMORE)
                socket.send_json({"angle_between_16_14_12": angle_between_16_14_12,
                                   "angle_between_14_12_24": angle_between_14_12_24,
                                  "shouldIjump": shouldIjump})



                socket.send_string("walking_placeblock", flags=zmq.SNDMORE)
                socket.send_json({"current_frame_angle_for_right_hip": angle_between_12_24_26,
                                   "current_frame_angle_for_left_hip": angle_between_11_23_25,
                                  "current_frame_angle_for_left_knee": angle_between_23_25_27_left,
                                  "current_frame_angle_for_right_knee": angle_between_24_26_28_right,
                                  "current_frame_right_hip_y_coordinate": right_hip_y_coordinate,
                                  "right_knee_y": right_ankle_y,
                                  "left_knee_y": left_ankle_y,
                                  "angle_rightknee_rightankle_leftankle": angle_rightknee_rightankle_leftankle,
                                  "angle_leftknee_lefttankle_rightankle": angle_leftknee_lefttankle_rightankle})

                socket.send_string("turnbody_swimming_eating", flags=zmq.SNDMORE)
                socket.send_json({"degree_theta": degree_theta,
                                  "stop_turning_body": stop_turning_body,
                                  "angle_between_14_12_24": angle_between_14_12_24})

                socket.send_string("choosing_mode", flags=zmq.SNDMORE)
                socket.send_json({"message1": 3,
                                  "message2": 5})




                execute_placeblock = 0

                #Visualisation
                cv2.putText(image, str(left_ankle_y),
                            tuple(np.multiply(left_shoulder_11, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 7, cv2.LINE_AA
                            )
            i = i+1
        except:
            pass

        # render
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))


        # print(results)
        cv2.imshow('Media Feed', image)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

