import cv2
from settings import __APP_SETTINGS__
from collections import deque
import numpy as np
import os
from datetime import date
import time

first_frame = None
next_frame = None
delay_counter = 0

def add_filters(frame):
    global first_frame, next_frame, delay_counter
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur it to remove camera noise (reducing false positives)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
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
    # Compare the two frames, find the difference
    frame_delta = cv2.absdiff(first_frame, next_frame)
    thresh = cv2.threshold(frame_delta, 20, 255, cv2.THRESH_BINARY)[1]
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
        




def make_vid(frame_width, frame_height, image_list, fps=3):
    current_date = date.today()
    current_time = int(time.time())

    video = cv2.VideoWriter(os.path.join(__APP_SETTINGS__.VIDEO_PATH, f"{current_date}-{current_time}.avi"), cv2.VideoWriter_fourcc(*'XVID'), 5, (frame_width, frame_height))

    for i in range(len(image_list)):
        video.write(image_list[i])

    video.release()
    print('Video Saved')



    os.path.join(__APP_SETTINGS__.VIDEO_PATH, f"{current_date}-{current_time}.avi")