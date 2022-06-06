import cv2
import numpy as np
from dlclive import DLCLive, Processor

folder = 'model/'
dlc_proc = Processor()
dlc_live = DLCLive(folder, processor=dlc_proc)
dlc_live.init_inference()

i = 0
radius = 15
thickness = -1


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

# Load frame
i += 1
frame = cv2.imread('frames/ ('+str(i)+').jpg')
#frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

# Get poses
pose = dlc_live.get_pose(frame)
nose = (int(pose[0, 0]), int(pose[0, 1]))
head = (int(pose[1, 0]), int(pose[1, 1]))
body = (int(pose[2, 0]), int(pose[2, 1]))

# Calculate distance and activation
target = (int(frame.shape[1]-5), int(frame.shape[0]/2))

# Draw Dots
for gx in range(1, frame.shape[1], 10):
    for gy in range(1, frame.shape[0], 10):
        length = cv2.norm(target, (gx, gy))
        pct = gaussian(length, 0, int(frame.shape[1]*.1))  # Collapse distance and run through 1d Gaussian
        frame = cv2.circle(frame, (gx, gy), int(radius*pct), (int(255*pct), int(255*pct), 0, .5), thickness)

cv2.imshow('Gaussian Test', frame)
cv2.waitKey(1000000)

