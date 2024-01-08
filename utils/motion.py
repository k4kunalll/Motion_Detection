import cv2
import imutils
from collections import deque
from settings import __APP_SETTINGS__
from utils.helper_functions import (
    add_filters,
    calc_diff,
    bbox,
    make_vid,
    filter_bboxes,
    excel_generator,
    create_log,
)
from datetime import date
import time
import threading

current_date = date.today()
current_time = int(time.time())


def motion(video_path):
    global centre_point, current_time, current_date
    roi_XminYmin = __APP_SETTINGS__.ROI_XY_MIN
    roi_XmaxYmax = __APP_SETTINGS__.ROI_XY_MAX
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    frame_list = []
    frame_no = 0  # Init frame variables
    first_frame = None
    next_frame = None
    centre_point = deque([], maxlen=__APP_SETTINGS__.DOTS_HISTORY)
    # used to record the time when we processed last frame
    prev_frame_time = 0
    # used to record the time at which we processed current frame
    new_frame_time = 0
    movement_persistent_counter = 0

    if cap.isOpened() is False:
        print("Error opening video file")
    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret is True:
            try:
                # frame_list = []
                text = "Unoccupied"
                frame_bool = False
                frame_no = frame_no + 1
                print("FrameNo:", frame_no)
                cv2.rectangle(frame, roi_XminYmin, roi_XmaxYmax, (0, 0, 0), 2)
                first_frame, next_frame = add_filters(frame)
                frame_diff = calc_diff(first_frame, next_frame)
                boxes = bbox(frame_diff, 1)

                # if boxes is not None:
                frame, frame_bool, centre_point = filter_bboxes(
                    frame, boxes, centre_point
                )
                # frame_list.append(frame)

                # frame_list.append(frame)

                if frame_bool is True:
                    movement_persistent_counter = (
                        __APP_SETTINGS__.MOVEMENT_DETECTED_PERSISTENCE
                    )

                if movement_persistent_counter > 0:
                    text = "Movement Detected " + str(movement_persistent_counter)
                    movement_persistent_counter -= 1
                    frame_list.append(frame)
                else:
                    text = f"No Movement Detected, {movement_persistent_counter}"

                if movement_persistent_counter == 1 and len(frame_list) >= __APP_SETTINGS__.FRAMESAVE_THRESH:
                    t1 = threading.Thread(
                        target=make_vid,
                        args=(
                            frame_width,
                            frame_height,
                            frame_list,
                            __APP_SETTINGS__.VIDEO_FPS,
                        ),
                    )
                    t1.start()
                    t1.join()
                    excel_generator()
                    frame_list = []
                    centre_point = deque([], maxlen=__APP_SETTINGS__.DOTS_HISTORY)

                if movement_persistent_counter == 1 and len(frame_list) <= __APP_SETTINGS__.FRAMESAVE_THRESH:
                    frame_list = []
                    centre_point = deque([], maxlen=__APP_SETTINGS__.DOTS_HISTORY)

                cv2.putText(
                    frame,
                    str(text),
                    (10, 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

                new_frame_time = time.time()
                fps = 1 / (new_frame_time - prev_frame_time)
                prev_frame_time = new_frame_time
                # converting the fps into integer
                fps = int(fps)
                # converting the fps to string so that we can display it on frame
                # by using putText function
                fps = str(fps)
                cv2.putText(
                    frame,
                    f"FPS: {fps}",
                    (10, 150),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.75,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

                # print("fps:", fps)
                # print("FRAMES FOR VIDEO --------->", len(frame_list))
                # cv2.imwrite(f"images/{frame_no}.jpg", frame)
                frame = imutils.resize(frame, width=1200)
                cv2.imshow("frame", frame)
                ch = cv2.waitKey(1)
                if ch & 0xFF == ord("q"):
                    break

            except Exception as e:
                create_log((e, "FRAMES FOR VIDEO --------->", len(frame_list)))
                break

        else:
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    motion(__APP_SETTINGS__.RTSP_LINK)
