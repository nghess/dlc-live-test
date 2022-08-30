import cv2
import numpy as np

i = 0
trajectory = []

while True:
    # Load frame
    i += 1
    frame = cv2.imread('frames/ ('+str(i)+').jpg')
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur and threshold to get smooth region
    blur = cv2.GaussianBlur(frame, (15, 15), cv2.BORDER_DEFAULT)
    ret, thresh = cv2.threshold(blur, 48, 255, 0)

    # Find mouse (2nd largest contour)
    contour = cv2.findContours(thresh, mode=1, method=1)
    mouse_c = []
    for element in reversed(contour[0]):
        if frame.shape[0]*2 > len(element) > frame.shape[0]/3:
            mouse_c = np.array(element)
            break

    # Get centroid of Mouse
    M = cv2.moments(mouse_c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    trajectory.extend([(cX, cY)])  # Add to list of centers

    # Draw cv2 shapes
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)  # Convert back to BGR
    frame = cv2.drawContours(frame, mouse_c, -1, color=(0, 255, 255), thickness=2, lineType=cv2.LINE_AA)  # Outline

    if len(trajectory) > 1:
        for c in range(1, len(trajectory)):  # Draw lines between centers in trajectory list
            image = cv2.line(frame, trajectory[c], trajectory[c-1], (0, 0, int((c/len(trajectory))*255), .01), 3, lineType=cv2.LINE_AA)

    frame = cv2.circle(frame, (cX, cY), 7, (255, 255, 0), -1, lineType=cv2.LINE_AA)  # Draw centroid

    # Show video
    cv2.imshow('Mouse Centroid', frame)
    cv2.imwrite("output/centroid/" + str(i) + ".png", frame)
    cv2.waitKey(1)

    # Reset loop
    if i == 999:
        i = 0
        trajectory = []
        break

