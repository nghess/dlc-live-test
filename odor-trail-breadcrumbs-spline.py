import cv2
import numpy as np
from dlclive import DLCLive, Processor
import os

# Initialize variables
i = 0   # frame counter
jitter = 0  # Jitter for curve points
rng = 117  # Set random seed
np.random.seed(rng)

def load_curve(crv_file, jitter=5):
    file = open(crv_file, "r")
    data = file.read()
    # Formatting as list
    crv_pts = data.replace('{', '[').replace('}', ']').split('\n')
    # converting to list of lists
    for p in range(len(crv_pts)):
        crv_pts[p] = eval(crv_pts[p])
        jit = np.random.normal(crv_pts[p], jitter)
        crv_pts[p] = jit
    return crv_pts

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

# Curve points file
crv_file = "curves/arena_crv.txt"

# Load curve
crv = load_curve(crv_file, jitter)
popper = crv

# Get video dimensions
dim_img = cv2.imread(frames_dir+' ('+str(1)+').png')
scale = .5
width = int(dim_img.shape[1]*scale)
height = int(dim_img.shape[0]*scale)
offset = (int(height/2), int(width/2))


while True:
    # Load frame
    i += 1
    frame = cv2.imread(frames_dir+' ('+str(i)+').png')
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
    frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)

    # Get nose
    pose = dlc_live.get_pose(frame)
    nose = (int(pose[0, 0]), int(pose[0, 1]))

    # Pop point if nose is close
    for c in range(len(crv)):
        if cv2.norm(nose, (crv[c][0], crv[c][1])) <= 12: #or nose[0] < crv[c][0] and nose[1] < crv[c][1]:
            popper = crv[c:]
    if len(popper) > 0:
        crv = popper

    # Draw curve
    for c in range(1, len(crv)):
        if c == 1:
            radius = 7
            color = (255, 255, 0)
        elif c == 2:
            radius = 2
            color = (255, 255, 0)
        else:
            radius = 1
            color = (200, 200, 200)
        center_c = (int(crv[c][0]), int(crv[c][1]))
        center_p = (int(crv[c-1][0]), int(crv[c-1][1]))
        frame = cv2.circle(frame, center_c, radius, color, -1, lineType=cv2.LINE_AA)

    # Show video
    cv2.imshow('Pose', frame)
    cv2.imwrite("output/breadcrumbs_jitter/" + str(i) + "_s" + str(rng) + ".png", frame)
    cv2.waitKey(1)

    # Reset loop
    if i == frames_count:
        crv = load_curve(crv_file, jitter)
        popper = crv
        i = 0
        break