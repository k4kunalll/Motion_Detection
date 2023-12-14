import cv2
import imutils
from collections import deque
from settings import __APP_SETTINGS__
from utils.helper_functions import add_filters, calc_diff, bbox

centre_point = deque([],maxlen=__APP_SETTINGS__.DOTS_HISTORY)

def main(video_path):
    global centre_point
    roi_XminYmin = __APP_SETTINGS__.ROI_XY_MIN
    roi_XmaxYmax = __APP_SETTINGS__.ROI_XY_MAX
    cap = cv2.VideoCapture(video_path)
    frame_no = 0 
    # Init frame variables
    first_frame = None
    next_frame = None
    if cap.isOpened() is False:
        print("Error opening video file")
    # Read until video is completed
    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret is True:
            frame_no = frame_no+1
            cv2.rectangle(frame, roi_XminYmin, roi_XmaxYmax, (0, 0, 0), 2)
            first_frame, next_frame = add_filters(frame)
            frame_diff = calc_diff(first_frame, next_frame)
            boxes = bbox(frame_diff,1)
            if boxes is not None:
                centroid = (int((boxes[0]+boxes[2])/2),int((boxes[1]+boxes[3])/2))

                if roi_XminYmin[0] < centroid[0] < roi_XmaxYmax[0] and roi_XminYmin[1] < centroid[1] < roi_XmaxYmax[1]:
                    centre_point.append(centroid)
                    cv2.rectangle(frame, (boxes[0],boxes[1]), (boxes[2],boxes[3]), (0, 255, 0), 2)
                    
            for i in range(len(centre_point)-1):
                if centre_point[i][1] - centre_point[i+1][1] < 0:
                    # print(centre_point[i][1] - centre_point[i+1][1], centre_point[i][0] - centre_point[i+1][0])
                    cv2.circle(frame,centre_point[i],1,(0, 0, 255), 3)

            frame = imutils.resize(frame, width = 1200)
            cv2.imshow("frame", frame)
            ch = cv2.waitKey(1)
            if ch & 0xFF == ord('q'):
                break
           
        # Break the loop
        else:
            break
    # When everything done, release
    # the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main("videos/Demo5.mp4")
