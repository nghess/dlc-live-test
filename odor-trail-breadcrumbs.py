import cv2
import numpy as np
from dlclive import DLCLive, Processor
import os

# Count files in frames folder
frames_count = 0
frames_dir = "frames/odor_trail/"
for path in os.listdir(frames_dir):
    if os.path.isfile(os.path.join(frames_dir, path)):
        frames_count += 1

# Initialize DLC-Live
folder = 'model/'
dlc_proc = Processor()
dlc_live = DLCLive(folder, processor=dlc_proc)
dlc_live.init_inference()
i = 0
trajectory = []

for x in range(frames_count):
    x += 1
    target = cv2.imread('frames/odor_trail/ ('+str(x)+').png')
    target = cv2.resize(target, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    # Get poses
    pose = dlc_live.get_pose(target)
    nose = (int(pose[0, 0]), int(pose[0, 1]))
    trajectory.extend([nose])  # Add to list of centers

print("breadcrumbs loaded")

while True:
    # Load frame
    i += 1
    frame = cv2.imread('frames/odor_trail/ ('+str(i)+').png')
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    #Draw Trajectory
    if len(trajectory) > 10:
        for k in range(len(trajectory)):
            if k % 10 != 0:
                trajectory[k] = (-10, -10)
        breadcrumbs = trajectory[i:]
        for c in range(1, len(breadcrumbs)):  # Draw dots between centers in trajectory list
            #frame = cv2.line(frame, breadcrumbs[c], breadcrumbs[c-1], (255, 255, 0), 20-c, lineType=cv2.LINE_AA)
            frame = cv2.circle(frame, breadcrumbs[c], 3, (255, 255, 0), -1, lineType=cv2.LINE_AA)

    # Show video
    cv2.imshow('Pose', frame)
    #cv2.imwrite("output/odor_trail/" + str(i) + ".png", frame)
    cv2.waitKey(1)

    # Reset loop
    if i == frames_count:
        i = 0
        #break