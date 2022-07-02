import cv2
import time
import numpy as np
from dlclive import DLCLive, Processor

folder = 'hand_model/'
dlc_proc = Processor()
dlc_live = DLCLive(folder, processor=dlc_proc)
dlc_live.init_inference()

i = 0
radius = 20
thickness = -1


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


# Start Camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")


while True:
    start_time = time.time()  # start time of the loop
    # Load frame
    i += 1
    ret, frame = cap.read()
    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)

    # Get poses
    pose = dlc_live.get_pose(frame)
    print(pose)
    wrist = (int(pose[0, 0]), int(pose[0, 1]))
    thmb1 = (int(pose[1, 0]), int(pose[1, 1]))
    thmb2 = (int(pose[2, 0]), int(pose[2, 1]))
    thmb3 = (int(pose[3, 0]), int(pose[3, 1]))
    thmb4 = (int(pose[4, 0]), int(pose[4, 1]))
    indx1 = (int(pose[5, 0]), int(pose[5, 1]))
    indx2 = (int(pose[6, 0]), int(pose[6, 1]))
    indx3 = (int(pose[7, 0]), int(pose[7, 1]))
    indx4 = (int(pose[8, 0]), int(pose[8, 1]))
    midl1 = (int(pose[9, 0]), int(pose[9, 1]))
    midl2 = (int(pose[10, 0]), int(pose[10, 1]))
    midl3 = (int(pose[11, 0]), int(pose[11, 1]))
    midl4 = (int(pose[12, 0]), int(pose[12, 1]))
    ring1 = (int(pose[13, 0]), int(pose[13, 1]))
    ring2 = (int(pose[14, 0]), int(pose[14, 1]))
    ring3 = (int(pose[15, 0]), int(pose[15, 1]))
    ring4 = (int(pose[16, 0]), int(pose[16, 1]))
    pink1 = (int(pose[17, 0]), int(pose[17, 1]))
    pink2 = (int(pose[18, 0]), int(pose[18, 1]))
    pink3 = (int(pose[19, 0]), int(pose[19, 1]))
    pink4 = (int(pose[20, 0]), int(pose[20, 1]))

    # Points
    points = [wrist, thmb1, thmb2, thmb3, thmb4, indx1, indx2, indx3, indx4, midl1, midl2, midl3, midl4, ring1, ring2,
              ring3, ring4, pink1, pink2, pink3, pink4]
    for point in points:
        i += 10
        frame = cv2.circle(frame, point, 3, (i, i, i+55), thickness)

    # Display FPS and Resolution
    fps = f"FPS: {round(1.0 / (time.time() - start_time))}"
    res = f"{frame.shape[0]}x{frame.shape[1]}px"
    frame = cv2.putText(frame, fps, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), lineType=cv2.LINE_AA)
    frame = cv2.putText(frame, res, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 0, 0), lineType=cv2.LINE_AA)

    # Show video
    cv2.imshow('Pose', frame)
    #cv2.imwrite("output/" + str(i) + ".png", frame)
    cv2.waitKey(1)
