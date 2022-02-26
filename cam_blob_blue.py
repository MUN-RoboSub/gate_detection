# imutils grabs the contours that have already formed
import numpy as np
import cv2
import imutils
import math
# getting the computers video capture
cap = cv2.VideoCapture(0)

while True:
    # reading the frames/cam
    _, frame = cap.read()
    

    # applying a gaussian blur to the cam so that it does not pick up background noise
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv_frame = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    
    # defining the upper and lower bounds for color
    lower_blue = np.array([38, 86, 0])
    upper_blue = np.array([121, 255, 255])
    
    # creating a blue hsv_frame mask so that only the specified range shows up
    blue_mask = cv2.inRange(hsv_frame, lower_blue, upper_blue)
    blue = cv2.bitwise_and(frame, frame, mask=blue_mask)

    # defining contours and setting imutils.grab_contours to get the already created contours
    contours = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = imutils.grab_contours(contours)
    centers = []
        
    for contour in contours:
        area = cv2.contourArea(contour)
        # print(area)
        # print(len(contours))
        # only display for blue things that are a specifed size
        if area > 800:
            cv2.drawContours(frame, [contour], -1, (0,255, 0), 3)

            # movements is used to plot points 
            M = cv2.moments(contour)
             
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            # creating the center point circle
            cv2.circle(frame, (cx,cy), 3, (255, 255, 255), -1)

            # adding center point to the contour  
            cv2.putText(frame,"Centre", (cx-20, cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255), 1)
            cv2.putText(frame,"("+str(cx)+","+str(cy)+")", (cx+10,cy+15), cv2.FONT_HERSHEY_SIMPLEX, 0.4,(0, 0, 255),1)
            # adding contour to the centers list, to create a list of all contour objects
            centers.append([cx, cy])
            
        if len(centers) == 2:
            # if there are two objects, it will get the center points of each object and plot them to create the distance line
            dx = centers[0][0] - centers[1][0]
            start_point = (centers[0][0], centers[0][1])
            end_point = (centers[1][0], centers[1][1])
            dy = centers[1][0] - centers[1][1]
            center_point = np.sqrt(dx*dx+dy*dy)
            print(f"Distance between: {center_point}")
            cv2.line(frame, start_point, end_point, (255,255,255), 2)
            print(f"start: {start_point}")
            print(f"end: {end_point}")
            
            

    # show cam with contours
    cv2.imshow("Frame", frame)
    # show blue mask
    cv2.imshow("Mask", blue)
    key = cv2.waitKey(1)
    if key == 27:
        break
    # cv2.imshow("Frame", frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #   break

cap.release()
cv2.destroyAllWindows()
