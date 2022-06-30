import cv2
import time
import numpy as np
from dlclive import DLCLive, Processor

folder = 'model/'
dlc_proc = Processor()
dlc_live = DLCLive(folder, processor=dlc_proc)
dlc_live.init_inference()

i = 0
radius = 20
thickness = -1

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


while True:
    start_time = time.time() # start time of the loop
    # Load frame
    i += 1
    frame = cv2.imread('frames/ ('+str(i)+').jpg')
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    # Get poses
    pose = dlc_live.get_pose(frame)
    nose = (int(pose[0, 0]), int(pose[0, 1]))
    head = (int(pose[1, 0]), int(pose[1, 1]))
    body = (int(pose[2, 0]), int(pose[2, 1]))

    #wind = nose[0]
    # Calculate distance and activation
    target = (int(frame.shape[1]-20), int(frame.shape[0]/2))
    length = cv2.norm(target, nose)
    laser = gaussian(length, 0, int(frame.shape[1]*.35))  # Collapse distance and run through 1d Gaussian

    # Draw Markers
    frame = cv2.line(frame, nose, target, (int(255*laser), int(255*laser), int(255*laser)))
    frame = cv2.circle(frame, nose, int(radius*laser), (int(255*laser), int(255*laser), 0), thickness)
    frame = cv2.circle(frame, target, 5, (0, 0, 255), thickness)

    # Display FPS and Resolution
    fps = f"FPS: {round(1.0 / (time.time() - start_time))}"
    res = f"{frame.shape[0]}x{frame.shape[1]}px"
    frame = cv2.putText(frame, fps, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), lineType=cv2.LINE_AA)
    frame = cv2.putText(frame, res, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 0, 0), lineType=cv2.LINE_AA)

    # Show video
    cv2.imshow('Pose', frame)
    #cv2.imwrite("output/" + str(i) + ".png", frame)
    cv2.waitKey(1)

    # Reset loop
    if i == 969:
        i = 0
