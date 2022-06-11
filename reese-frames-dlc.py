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
flow = 0

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


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
    if nose[0] > head[0]:
        tilt = cv2.norm(head, nose)
        flow = (nose[0]-head[0])/tilt
    else:
        flow = 0

    #wind = nose[0]
    # Calculate distance and activation
    target = (int(frame.shape[1]-20), int(frame.shape[0]/2))
    length = cv2.norm(target, nose)
    laser = gaussian(length, 0, int(frame.shape[1]*.35))  # Collapse distance and run through 1d Gaussian

    # Draw dot
    #frame = cv2.line(frame, nose, target, (int(255*laser), int(255*laser), int(255*laser)))
    #frame = cv2.line(frame, head, body, (int(255*laser), int(255*laser), 255), 2)
    #frame = cv2.line(frame, nose, head, (int(255*laser), int(255*laser), 0), 1)
    #frame = cv2.circle(frame, nose, int(radius*laser), (int(255*laser), int(255*laser), 255), thickness)
    frame = cv2.circle(frame, nose, int(radius*flow*laser), (int(255*flow), int(255*flow), 0), thickness)



    # Show video
    cv2.imshow('Pose', frame)
    #cv2.imwrite("output/" + str(i) + ".png", frame)
    cv2.waitKey(1)

    # Reset loop
    if i == 969:
        i = 0
