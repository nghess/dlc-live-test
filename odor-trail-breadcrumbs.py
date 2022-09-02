import cv2
import numpy as np
from dlclive import DLCLive, Processor
import os

# Count files in frames folder
frames_count = 0
frames_dir = "frames/breadcrumbs/"
for path in os.listdir(frames_dir):
    if os.path.isfile(os.path.join(frames_dir, path)):
        frames_count += 1

# Initialize DLC-Live
folder = 'model/'
dlc_proc = Processor()
dlc_live = DLCLive(folder, processor=dlc_proc)
dlc_live.init_inference()

# Initialize variables
i = 0
trajectory = []
spacing = 7

for x in range(frames_count):
    x += 1
    target = cv2.imread(frames_dir+' ('+str(x)+').png')
    target = cv2.resize(target, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    # Get poses
    pose = dlc_live.get_pose(target)
    nose = (int(pose[0, 0]), int(pose[0, 1]))
    trajectory.extend([nose])  # Add to list of centers

print("Breadcrumbs Loaded...")

while True:
    # Load frame
    i += 1
    frame = cv2.imread(frames_dir+' ('+str(i)+').png')
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    #Draw Trajectory
    if len(trajectory) > spacing:
        for k in range(len(trajectory)):
            if k % spacing != 0:
                trajectory[k] = (-10, -10)
        #    else:
        #  add to dictionary for frame:line combos?

        breadcrumbs = trajectory[i:]
        for c in range(1, len(breadcrumbs)):  # Draw dots between centers in trajectory list
            #frame = cv2.line(frame, breadcrumbs[c], breadcrumbs[c-1], (0, 0, 0), 1, lineType=cv2.LINE_AA)
            color = (255-int((c/len(breadcrumbs))*255), 255-int((c/len(breadcrumbs))*255), 0)
            #color = (255, 255, 0)
            #radius = 5-int((c/len(breadcrumbs))*5)+1
            radius = 3
            frame = cv2.circle(frame, breadcrumbs[c], radius, color, -1, lineType=cv2.LINE_AA)

    # Show video
    cv2.imshow('Pose', frame)
    cv2.imwrite("output/breadcrumbs/" + str(i) + ".png", frame)
    cv2.waitKey(1)

    # Reset loop
    if i == frames_count:
        i = 0
        #break