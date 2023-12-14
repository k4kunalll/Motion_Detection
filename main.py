import cv2
import imutils
from collections import deque
from settings import __APP_SETTINGS__
from utils.helper_functions import add_filters, calc_diff, bbox, make_vid, filter_bboxes, excel_generator
import random
from datetime import date
import time


current_date = date.today()
current_time = int(time.time())


def main(video_path):
    global centre_point, current_time, current_date
    roi_XminYmin = __APP_SETTINGS__.ROI_XY_MIN
    roi_XmaxYmax = __APP_SETTINGS__.ROI_XY_MAX
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(3)) 
    frame_height = int(cap.get(4))
    frame_list = []
    frame_no = 0   # Init frame variables
    motion_start = 0
    motion_end = 0
    motion_start_temp = None
    first_frame = None
    next_frame = None
    if cap.isOpened() is False:
        print("Error opening video file")
    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret is True:
            # frame_list = []
            frame_no = frame_no+1
            cv2.rectangle(frame, roi_XminYmin, roi_XmaxYmax, (0, 0, 0), 2)
            first_frame, next_frame = add_filters(frame)
            frame_diff = calc_diff(first_frame, next_frame)
            boxes = bbox(frame_diff,1)
            if boxes is not None:
                frame, motion_start, motion_end = filter_bboxes(frame, boxes, motion_start, motion_end)
                frame_list.append(frame)

            else:
                motion_end = motion_end+1

            if motion_start == __APP_SETTINGS__.VIDEO_SAVE_FRAMES_THRESH:
                make_vid(frame_width, frame_height, frame_list)
                excel_generator()
                frame_list = []
                motion_start = 0

            print("FrameNo:",frame_no)
            print("--------------->",len(frame_list))
            print(motion_start, motion_end, motion_start_temp)
            cv2.imwrite(f"images/{frame_no}.jpg", frame)
            frame = imutils.resize(frame, width = 1200)
            cv2.imshow("frame", frame)
            ch = cv2.waitKey(1)
            if ch & 0xFF == ord('q'):
                break

        else:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main("videos/Demo.mp4")
