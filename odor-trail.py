import cv2
import numpy as np
from dlclive import DLCLive, Processor

folder = 'model/'
dlc_proc = Processor()
dlc_live = DLCLive(folder, processor=dlc_proc)
dlc_live.init_inference()
i = 0
trajectory = []

while True:
    # Load frame
    i += 1
    target = cv2.imread('frames/odor_trail/ ('+str(i+10)+').png')
    frame = cv2.imread('frames/odor_trail/ ('+str(i)+').png')
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    target = cv2.resize(target, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    # Get poses
    pose = dlc_live.get_pose(target)
    nose = (int(pose[0, 0]), int(pose[0, 1]))
    trajectory.extend([nose])  # Add to list of centers

    #Draw Trjaectory
    if len(trajectory) > 1:
        trajectory = trajectory[-10:]
        for c in range(1, len(trajectory)):  # Draw lines between centers in trajectory list
            image = cv2.line(frame, trajectory[c], trajectory[c-1], (int((c/len(trajectory))*255), int((c/len(trajectory))*255), 0), 20-c, lineType=cv2.LINE_AA)


    # Show video
    cv2.imshow('Pose', frame)
    cv2.imwrite("output/odor_trail/" + str(i) + ".png", frame)
    cv2.waitKey(1)

    # Reset loop
    if i == 533:
        break
        #i = 0