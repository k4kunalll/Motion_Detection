import imutils
import cv2
import numpy as np
from settings import __APP_SETTINGS__
from collections import defaultdict, deque
from tracker import bb_intersection_over_union
import os

roi_XminYmin = (357,466)
roi_XmaxYmax = (2038,1103)


# Init frame variables
first_frame = None
next_frame = None

# Init display font and timeout counters
font = cv2.FONT_HERSHEY_SIMPLEX
delay_counter = 0
frane_no = 0
centre_point = deque([],maxlen=300)
coor = deque([],maxlen=2)

# Create capture object
cap = cv2.VideoCapture('videos/Demo5.mp4') # Then start the webcam

# Check if camera opened successfully 
if (cap.isOpened() is False): 
    print("Error opening video file")

while(cap.isOpened()): 
    
    # Set transient motion detected as false
    transient_movement_flag = False
    
    # Read frame
    ret, frame = cap.read()
    if ret is True: 
        frane_no = frane_no+1
        temp_frames = []
        cv2.rectangle(frame, roi_XminYmin, roi_XmaxYmax, (0, 0, 0), 2)
        # Resize and save a greyscale version of the image
        # frame = imutils.resize(frame, width = 700)

        # Create the sharpening kernel 
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) 
        
        # Sharpen the image 
        sharpened_image = cv2.filter2D(frame, -1, kernel) 

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Blur it to remove camera noise (reducing false positives)
        gray = cv2.GaussianBlur(gray, (3, 3), 0)

        # If the first frame is nothing, initialise it
        if first_frame is None: first_frame = gray    

        delay_counter += 1

        # Otherwise, set the first frame to compare as the previous frame
        # But only if the counter reaches the appriopriate value
        # The delay is to allow relatively slow motions to be counted as large
        # motions if they're spread out far enough
        if delay_counter > __APP_SETTINGS__.FRAMES_TO_PERSIST:
            delay_counter = 0
            first_frame = next_frame

                # Set the next frame to compare (the current frame)prin
        next_frame = gray

        # Compare the two frames, find the difference
        frame_delta = cv2.absdiff(first_frame, next_frame)
        thresh = cv2.threshold(frame_delta, 20, 255, cv2.THRESH_BINARY)[1]

        # Fill in holes via dilate(), and find contours of the thesholds
        thresh = cv2.dilate(thresh, None, iterations = 2)
        cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # loop over the contours
        for c in cnts:

            # Save the coordinates of all found contours
            (x, y, w, h) = cv2.boundingRect(c)
            coor.append([x, y,x + w, y + h])

            # If the contour is too small, ignore it, otherwise, there's transient
            # movement
            # print(cv2.contourArea(c))
            if cv2.contourArea(c) >= __APP_SETTINGS__.MIN_SIZE_FOR_MOVEMENT:
                transient_movement_flag = True

                centroid = (int((x+x+w)/2),int((y+y+h)/2))

                if roi_XminYmin[0] < centroid[0] < roi_XmaxYmax[0] and roi_XminYmin[1] < centroid[1] < roi_XmaxYmax[1]:
                    # print(bb_intersection_over_union(coor[0],coor[1]))
                    centre_point.append(centroid)
                    try:
                        if centre_point[0][1]-centre_point[1][1] < 0:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    except:
                        pass
                    # print(x, y,x + w, y + h)
                # Draw a rectangle around big enough movements
                    # cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # for ct in centre_point:
        #     print(centre_point)
        #     cv2.circle(frame,ct,1,(0, 0, 255), -1)

        for i in range(len(centre_point)-1):
            if centre_point[i][1] - centre_point[i+1][1] < 0:
                print(centre_point[i][1] - centre_point[i+1][1], centre_point[i][0] - centre_point[i+1][0])
                cv2.circle(frame,centre_point[i],1,(0, 0, 255), 3)

        
        
    #     # Splice the two video frames together to make one long horizontal one
        cv2.imwrite(f"images/{frane_no}.jpg", frame)
        frame = imutils.resize(frame, width = 1200)
        cv2.imshow("frame", frame)
        

        ch = cv2.waitKey(1)
        if ch & 0xFF == ord('q'):
            break

# Cleanup when closed
cv2.waitKey(0)
cv2.destroyAllWindows()
cap.release()


# working
