import cv2
import numpy as np
from dlclive import DLCLive, Processor
from skimage.transform import (hough_line, hough_line_peaks)

folder = 'model/'
dlc_proc = Processor()
dlc_live = DLCLive(folder, processor=dlc_proc)
dlc_live.init_inference()

i = 0

while True:
    # Load frame
    i += 1
    frame = cv2.imread('frames/ ('+str(i)+').jpg')
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    # Get poses
    pose = dlc_live.get_pose(frame)
    nose = (int(pose[0, 0]), int(pose[0, 1]))
    head = (int(pose[1, 0]), int(pose[1, 1]))
    body = (int(pose[2, 0]), int(pose[2, 1]))

    # Draw lines on Stage for angle measurement
    stage = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)  # Clear frame
    stage = cv2.line(stage, nose, head, 255, 1)

    # Perform Hough Transformation to detect lines
    hspace, angles, distances = hough_line(stage)

    # Find angle
    angle = []
    for _, a, distances in zip(*hough_line_peaks(hspace, angles, distances)):
        angle.append(a)

    # Obtain angle for each line
    angles = [a*180/np.pi for a in angle]

    # Get length of radius for angle visualization
    radius = cv2.norm(head, nose)
    axes = (int(radius), int(radius))

    # Draw lines
    frame = cv2.line(frame, nose, head, (255, 255, 0), 2)
    frame = cv2.line(frame, (head[0], frame.shape[0]), (head[0], 0), (0, 0, 0), 1)
    frame = cv2.putText(frame, str(int(angles[0])), (head[0]-50, head[1]-50), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255))

    # Conditionals to draw the radius on correct quadrant
    if nose[0] > head[0]:
        if angles[0] > 0:
            frame = cv2.ellipse(frame, head, axes, -90, angles[0], 0, (0, 0, 255))
        else:
            frame = cv2.ellipse(frame, head, axes, 90, angles[0], 0, (0, 0, 255))
    else:
        if angles[0] > 0:
            frame = cv2.ellipse(frame, head, axes, 90, angles[0], 0, (0, 0, 255))
        else:
            obtuse = int(90 - angles[0])
            frame = cv2.ellipse(frame, head, axes, -90, angles[0], 0, (0, 0, 255))

    # Show video
    cv2.imshow('Pose', frame)
    cv2.imwrite("output/" + str(i) + ".png", frame)
    cv2.waitKey(1)

    # Reset loop
    if i == 969:
        i = 0
        break