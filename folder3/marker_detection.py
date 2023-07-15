import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#erosion and dialation
kernel1 = np.ones((5,5), dtype = 'uint8')
kernel2 = np.ones((3, 3), dtype = 'uint8')

l=[]

#boolean variable which decides whether to start painting or not
paint = False

#while loop for editing the video frame by frame
while True:
    key = cv2.waitKey(1)
    #setting point to true if p is pressed on the keyboard
    if key == ord('p'):
        paint = True

    ret, frame = cap.read()

    #making the frame a mirror image
    frame = cv2.flip(frame, 1)
    #Converting to HSV to create a mask and filter out the color(blue, in this case)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    

    #creating the mask
    low = np.array([95, 160, 121], dtype = 'uint8')
    high = np.array([121, 255, 255], dtype = 'uint8')

    mask = cv2.inRange(hsv, low, high)

    erode = cv2.erode(mask, kernel1, iterations = 1)
    dilate = cv2.dilate(erode, kernel1, iterations = 1)
    dilate = cv2.dilate(dilate, kernel2, iterations = 3)

    #no value to the code - used for visualizing the mask
    #img2 = cv2.bitwise_and(frame, mask = dilate)

    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    if len(contours)>0:
        x, y, h, w = cv2.boundingRect(contours[0])
        x1 = int(x+h/2+20)
        y1 = int(y+(w/2))
        cv2.circle(frame, (x1, y1), 15, (0, 0, 255), -1)
        if paint:
            l.append((x1, y1))
    else: 
        pass

    #if paint is true, drawing on the captured frame
    if paint:
        for x2, y2 in l:
            #changing the color of the circle
            cv2.circle(frame, (x2, y2), 5,(105, 105, 105), -1)
            #connecting the lines between the circles
            if len(l)>1:
                for i in range(1, len(l)):
                    cv2.line(frame, (l[i-1][0], l[i-1][1]), (l[i][0], l[i][1]), (200, 127, 75), 5)

    #displaying output
    cv2.imshow('window', frame)

    #cv2.imshow('win', img2)
    #cv2.imshow('mask', dilate)

    #exit key for program
    if key == ord('q'):
        break
    
#releasing and destroying all windows
cap.release()
cv2.waitKey(3000)
cv2.destroyAllWindows()