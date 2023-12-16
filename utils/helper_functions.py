import cv2
from settings import __APP_SETTINGS__
from collections import deque
import numpy as np
import os
from datetime import date,datetime
import time
import pandas as pd
import math

first_frame = None
next_frame = None
delay_counter = 0
# centre_point = deque([],maxlen=__APP_SETTINGS__.DOTS_HISTORY)

def add_filters(frame):
    global first_frame, next_frame, delay_counter
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur it to remove camera noise (reducing false positives)
    gray = cv2.GaussianBlur(gray, __APP_SETTINGS__.BLUR_KERNEL, 0)
    # If the first frame is nothing, initialise it
    if first_frame is None:
        first_frame = gray
    delay_counter += 1
    if delay_counter > __APP_SETTINGS__.FRAMES_TO_PERSIST:
        delay_counter = 0
        first_frame = next_frame
    # Set the next frame to compare (the current frame)prin
    next_frame = gray
    return first_frame, next_frame


def calc_diff(first_frame, next_frame):
    DILATION_KERNEL = __APP_SETTINGS__.DILATION_KERNEL
    # Compare the two frames, find the difference
    frame_delta = cv2.absdiff(first_frame, next_frame)
    thresh = cv2.threshold(frame_delta, DILATION_KERNEL[0], DILATION_KERNEL[1], cv2.THRESH_BINARY)[1]
    # Fill in holes via dilate(), and find contours of the thesholds
    thresh = cv2.dilate(thresh, None, iterations=2)
    return thresh


def bbox(thresh_dilate, area_thresh):
    contours, _ = cv2.findContours(
        thresh_dilate.copy(),
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,  # cv2.RETR_TREE,
    )

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if cv2.contourArea(cnt) > area_thresh:
            return np.array([x, y, x + w, y + h])
        


def make_vid(frame_width, frame_height, image_list, fps=10):
    current_date = date.today()
    current_time = int(time.time())
    if not os.path.exists(__APP_SETTINGS__.VIDEO_PATH):
        os.makedirs(__APP_SETTINGS__.VIDEO_PATH)
    video = cv2.VideoWriter(os.path.join(__APP_SETTINGS__.VIDEO_PATH, f"{current_date}-{current_time}.mp4"), cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))
    for i in range(len(image_list)):
        video.write(image_list[i])

    video.release()
    print('Video Saved')


def filter_bboxes(frame, boxes_coor, motion_end, centre_point):
    # global centre_point
    frame_pass = False
    print("motion_end",motion_end)
    centroid = (int((boxes_coor[0]+boxes_coor[2])/2),int((boxes_coor[1]+boxes_coor[3])/2))


    if __APP_SETTINGS__.ROI_XY_MIN[0] < centroid[0] < __APP_SETTINGS__.ROI_XY_MAX[0] and __APP_SETTINGS__.ROI_XY_MIN[1] < centroid[1] < __APP_SETTINGS__.ROI_XY_MAX[1]:
            centre_point.append(centroid)
            cv2.rectangle(frame, (boxes_coor[0],boxes_coor[1]), (boxes_coor[2],boxes_coor[3]), (0, 255, 0), 2)
    else:
        if motion_end >= 15:
            centre_point = deque([],maxlen=__APP_SETTINGS__.DOTS_HISTORY)
    # else:
    #     centre_point.append((0,0))
    # for i in range(len(centre_point)-1):
    #     if centre_point[i][1] - centre_point[i+1][1] < 0:
    #         # print(centre_point[i][1] - centre_point[i+1][1], centre_point[i][0] - centre_point[i+1][0])
    #         cv2.circle(frame,centre_point[i],1,(0, 0, 255), 3)
            
    for i in range(len(centre_point)-1):
        if centre_point[i][1] - centre_point[i+1][1] < 0:
            cv2.circle(frame,centre_point[i],1,(0, 0, 255), 3)
            point_distance = int(math.hypot(centre_point[i+1][0] - centre_point[i][0], centre_point[i+1][1] - centre_point[i][1]))
            # print("Distance------------------>", point_distance)
            if __APP_SETTINGS__.MIN_MIX_DIST[0] < point_distance < __APP_SETTINGS__.MIN_MIX_DIST[1]:
                frame_pass = True 
                # print("Distance------------------>", point_distance)
                # cv2.circle(frame,centre_point[i],1,(0, 0, 255), 3)
                # cv2.rectangle(frame, (boxes_coor[0],boxes_coor[1]), (boxes_coor[2],boxes_coor[3]), (0, 255, 0), 2)
        # else:
        #     frame_pass = False
    
    


    return frame, frame_pass, centre_point


def excel_generator():
    if not os.path.exists(__APP_SETTINGS__.EXCEL_DIR):
        os.makedirs(__APP_SETTINGS__.EXCEL_DIR)
    if not os.path.exists(os.path.join(__APP_SETTINGS__.EXCEL_DIR,__APP_SETTINGS__.EXCEL_NAME)):
        df = pd.DataFrame(columns=['Date','Time'])
        df.to_csv(os.path.join(__APP_SETTINGS__.EXCEL_DIR,__APP_SETTINGS__.EXCEL_NAME), index=False, header=True)

    data_dict = [{"Date":date.today(),
                "Time":datetime.now().strftime("%H:%M:%S")}]
    df = pd.DataFrame.from_dict(data_dict)
    df.to_csv(os.path.join(__APP_SETTINGS__.EXCEL_DIR,__APP_SETTINGS__.EXCEL_NAME), index=False, header=False, mode="a")



    