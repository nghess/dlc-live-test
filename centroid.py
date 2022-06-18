import cv2
import numpy as np

i = 0


while True:
#for i in range(1,2):
    # Load frame
    i += 1
    frame = cv2.imread('frames/ ('+str(i)+').jpg')
    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur and threshold to get smooth region
    blur = cv2.GaussianBlur(frame, (21, 21), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(blur, 48, 255, 0)

    # Find mouse (2nd largest contour)
    contour = cv2.findContours(thresh, mode=1, method=1)
    mouse_c = []
    for element in contour[0]:
        if frame.shape[0]*2 > len(element) > frame.shape[0]/3:
            mouse_c = np.array(element)
            break

    # Get centroid of Mouse
    M = cv2.moments(mouse_c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    frame = cv2.drawContours(frame, mouse_c, -1, color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
    frame = cv2.circle(frame, (cX, cY), 5, (255, 255, 0), -1)

# Show video
    cv2.imshow('Pose', frame)
    #cv2.imwrite("output/" + str(i) + ".png", frame)
    cv2.waitKey(1)

    # Reset loop
    if i == 969:
        i = 0
