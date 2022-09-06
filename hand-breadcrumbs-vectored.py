import cv2
import time
import numpy as np
from dlclive import DLCLive, Processor

folder = 'hand_model/'
dlc_proc = Processor()
dlc_live = DLCLive(folder, processor=dlc_proc)
dlc_live.init_inference()

radius = 4
thickness = -1


def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def skeleton(start, end, canvas):
    for joint in range(start, end):
        canvas = cv2.line(canvas, points[joint], points[joint+1], (255, 128, 255), 1, lineType=cv2.LINE_AA)

# Start Camera
cap = cv2.VideoCapture(0)

# Check if the camera is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

thmb_l = 0
indx_l = 0
midl_l = 0
ring_l = 0
pink_l = 0

c = 0
scale = 1

dot = (320, 240)
hand_vec = []

while True:
    start_time = time.time()  # start time of the loop
    # Load frame
    i = 0
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    # Get poses
    pose = dlc_live.get_pose(frame)
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

    # Draw hand bound and centroid
    overlay = np.zeros((frame.shape[0], frame.shape[1], 3), np.uint8)  # Clear frame for overlay
    alpha = 0.4  # Transparency factor
    hand_bounds = np.array([indx4, pink4, pink1, indx1])
    hand1 = np.add(indx4, pink4)
    hand2 = np.add(pink1, indx1)
    hand3 = np.add(hand1, hand2) # Fix this
    hand_center = (hand3[0]/4, hand3[1]/4)
    cv2.drawContours(overlay, [hand_bounds], 0, (255, 255, 255), -1)
    #frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
    #frame = cv2.circle(frame, (int(hand_center[0]), int(hand_center[1])), 5, (255, 0, 0), -1, lineType=cv2.LINE_AA)

    hand_vec.append(hand_center)
    if len(hand_vec) > 2:
        hand_vec = hand_vec[1:]
    print(hand_vec)



    padding = 50
    # Generate dot
    if cv2.norm(hand_center, dot) < 45:
        dot = np.random.normal(hand_center, 75)
        if dot[0] < 0:
            dot[0] += padding
        if dot[0] > frame.shape[1]:
            dot[0] -= padding
        if dot[1] < 0:
            dot[1] += padding
        if dot[1] > frame.shape[0]:
            dot[1] -= padding

    frame = cv2.circle(frame, (int(dot[0]), int(dot[1])), 5, (0, 255, 255), -1, lineType=cv2.LINE_AA)


    # Display FPS and Resolution
    fps = f"FPS: {round(1.0 / (time.time() - start_time))}"
    res = f"{frame.shape[1]}x{frame.shape[0]}px"
    frame = cv2.putText(frame, fps, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255), lineType=cv2.LINE_AA)
    frame = cv2.putText(frame, res, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 0), lineType=cv2.LINE_AA)

    # Show video
    c += 1
    cv2.imshow('Pose', frame)
    cv2.imwrite("output/live/" + str(c) + ".png", frame)
    cv2.waitKey(1)
