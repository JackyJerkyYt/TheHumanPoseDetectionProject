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
        theta = 2*3.141596 + theta
    return theta * 180 / 3.141596

#Open cv
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
cap = cv2.VideoCapture(0)

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


            # Get Coordinates

            right_shoulder_12 = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                 landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]

            left_shoulder_11 = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                                landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]

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

            right_hip_y_coordinate = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y

            left_hip_y_coordinate = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y

            left_hand_x = landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].x

            left_hand_y = landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].y

            left_hand_z = landmarks[mp_pose.PoseLandmark.LEFT_INDEX.value].z

            left_elbow_x = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x

            left_elbow_y = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y

            right_hip_y = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y

            right_shoulder_y = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y

            right_elbow_y = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y

            mouth_x = landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value].x

            mouth_y = landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value].x

            right_hand_y = landmarks[mp_pose.PoseLandmark.RIGHT_INDEX.value].y

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
            angle_between_rightwrist_rightelbow_leftelbow = calculateangle(right_hand, right_elbow_14, left_elbow_13)

            ########################## turning body varaible

            degree_theta = new_calculate_angle()
            socket.send_pyobj([right_hip_y_coordinate,#0
                       left_hip_y_coordinate,#1
                       left_hand_x,#2
                       left_hand_y,#3
                       left_hand_z,#4
                       left_elbow_x,#5
                       left_elbow_y,#6
                       right_hip_y,#7
                       right_shoulder_y,#8
                       right_elbow_y,#9
                       mouth_x,#10
                       mouth_y,#11
                       angle_between_16_14_12,#12
                       angle_between_15_13_11,#13
                       angle_between_14_12_24,#14
                       angle_between_11_23_25,#15
                       angle_between_12_24_26,#16
                       angle_between_23_25_27_left,#17
                       angle_between_24_26_28_right,#18
                       angle_between_leftshoulder_leftelbow_leftwrist,#19
                       angle_between_rightshoulder_leftelbow_leftwrist,#20
                       angle_between_rightelbow_leftelbow_leftshoulder,#21
                       angle_between_rightwrist_rightelbow_leftelbow,#22
                       degree_theta,#23
                        right_hand_y])#24

            print("Sent")

            ##Visualisation
            cv2.putText(image, str(degree_theta),
                        tuple(np.multiply(left_shoulder_11, [640, 480]).astype(int)),
                        cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 0), 7, cv2.LINE_AA
                        )

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

