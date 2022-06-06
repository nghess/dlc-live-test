import cv2
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
    i += 1
    frame = cv2.imread('frames/ ('+str(i)+').jpg')
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    # Get poses
    pose = dlc_live.get_pose(frame)
    nose = (int(pose[0, 0]), int(pose[0, 1]))
    head = (int(pose[1, 0]), int(pose[1, 1]))
    body = (int(pose[2, 0]), int(pose[2, 1]))

    # Calculate distance and activation
    target = (int(frame.shape[1]-5), int(frame.shape[0]/2))
    distance = tuple(map(lambda k, v: abs(k - v), target, nose))
    x = round((target[1]-distance[1])/target[1], 2)  # X distance as percent of frame
    y = round((target[0]-distance[0])/target[0], 2)  # Y distance as percent of frame
    pct = gaussian(x*y, 1, .25)  # Collapse distance and run through 1d Gaussian

    # Draw Dots
    frame = cv2.circle(frame, nose, int(radius*pct), (int(255*pct), int(255*pct), 0, .5), thickness)
    #frame = cv2.circle(frame, head, radius, (0, 255, 0), thickness)
    #frame = cv2.circle(frame, body, radius, (0, 0, 255), thickness)
    #frame = cv2.circle(frame, target, radius, (0, 128, 255), thickness)

    cv2.imshow('Pose', frame)

    cv2.waitKey(1)
    if i == 999:
        i = 0
