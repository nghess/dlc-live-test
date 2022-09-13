import cv2
import numpy as np
import random

# Initialize variables
change = 1   # Amount to change jitter by
jitter = 0  # Jitter for curve points
jit_ceil = 10
rng = 117  # Set random seed
np.random.seed(rng)
random.seed(rng)

# Get video dimensions
frames_dir = "stills/"
arena = cv2.imread(frames_dir+'blank_arena.jpg')
arena = cv2.cvtColor(arena, cv2.COLOR_BGR2GRAY)
arena = cv2.cvtColor(arena, cv2.COLOR_GRAY2BGR)
scale = 1
height = arena.shape[1]
width = arena.shape[0]
origin = [int(height/2), int(width/2)]


def load_curve(crv_file, jitter=5, bounds=arena.shape, padding=50):
    file = open(crv_file, "r")
    data = file.read()
    # Formatting as list
    crv_pts = data.replace('{', '[').replace('}', ']').split('\n')
    # Converting to list of lists
    for p in range(len(crv_pts)):
        crv_pts[p] = eval(crv_pts[p])
    # Jitter points
    for p in range(1, len(crv_pts)-1):
        jit = np.random.normal(crv_pts[p], jitter)
        crv_pts[p] = jit
        if crv_pts[p][0] < 0:
            crv_pts[p][0] += padding
        if crv_pts[p][0] > arena.shape[1]:
            crv_pts[p][0] -= padding
        if crv_pts[p][1] < 0:
            crv_pts[p][1] += padding
        if crv_pts[p][1] > arena.shape[0]:
            crv_pts[p][1] -= padding
    return crv_pts


def orbit(dist, b1, rad):
    b2 = (b1[0]+dist, b1[1])
    c = (b2[0]-b1[0], b2[1] - b1[1])
    c = (int(c[0] * np.cos(rad) - c[1] * np.sin(rad)), int(c[0] * np.sin(rad) + c[1] * np.cos(rad)))
    c = (c[0]+b1[0], c[1]+b1[1])
    return c

def angle_btw(u, v, degrees=False):
    nu = np.linalg.norm(u)
    nv = np.linalg.norm(v)
    theta = np.arccos(np.dot(u, v)/(nu*nv))
    if degrees:
        theta = theta*(180/np.pi)
    return theta


def rand_segment(p1, p2, strength, seed):
    #weight = np.random.normal(.5, spread)
    random.seed(seed)
    weight = random.uniform(-.5, .5)*strength+.5
    rand_seg = np.add((1-weight)*np.array(p1), weight*np.array(p2))
    return (int(rand_seg[0]), int(rand_seg[1]))

# Curve points file
crv_file = "curves/sample_crv.txt"

strength = 0  # Strength of jitter. Stars at zero.
i = 0
count = 0
seeds = []  # List for predefined jitter seeds.
j_pts = []  # List for previous jittered point.

while True:
    i += 1
    count = 0
    #img = cv2.imread(frames_dir+'blank_arena.jpg')
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = np.zeros((width, height, 3), np.uint8)
    crv = load_curve(crv_file, jitter)
    if len(seeds) <= len(crv):
        for pt in range(1, len(crv)):
            seeds.append(random.uniform(0, 1000))

    # Draw curve
    for c in range(1, len(crv)):
        radius = 3
        color = (32, 32, 32)

        # Current and previous points
        center_c = (int(crv[c][0]), int(crv[c][1]))
        center_p = (int(crv[c-1][0]), int(crv[c-1][1]))
        # Draw true curve
        img = cv2.line(img, center_c, center_p, color, 2, lineType=cv2.LINE_AA)

    for c in range(1, len(crv)-1):
        radius = 3
        color = (128, 128, 255)
        count += 1

        # Current and previous points
        center_c = (int(crv[c][0]), int(crv[c][1]))
        center_p = (int(crv[c-1][0]), int(crv[c-1][1]))

        # Compute normals
        u = center_c
        v = [center_c[0], center_c[1]-50]
        pt1 = v
        pt2 = center_p
        u = np.subtract(pt1, center_c)
        v = np.subtract(pt2, center_c)
        rad = angle_btw(u, v)

        normal1 = orbit(cv2.norm(pt2, center_c), center_c, rad)
        normal2 = orbit(cv2.norm(pt2, center_c), center_c, rad+np.pi)

        # Draw normals
        img = cv2.line(img, center_c, normal1, (64, 64, 64), 1, lineType=cv2.LINE_AA)
        img = cv2.line(img, center_c, normal2, (64, 64, 64), 1, lineType=cv2.LINE_AA)
        img = cv2.circle(img, normal1, 2, (64, 64, 64), -1, lineType=cv2.LINE_AA)
        img = cv2.circle(img, normal2, 2, (64, 64, 64), -1, lineType=cv2.LINE_AA)
        img = cv2.putText(img, str(round(rad*(180/np.pi))), (center_p[0]+10, center_p[1]+10), cv2.FONT_HERSHEY_SIMPLEX, .25, (255, 255, 255))


        # Reference points to measure angle against
        #img = cv2.circle(img, pt1, 1, (0, 255, 0), -1, lineType=cv2.LINE_AA)
        #img = cv2.circle(img, pt2, 3, (0, 128, 128), -1, lineType=cv2.LINE_AA)


        # Add Jitter to points
        if count == 1 or count == len(crv)-2:
            j_pt = rand_segment(normal1, normal2, 0, seeds[c-1])
        else:
            j_pt = rand_segment(normal1, normal2, strength, seeds[c - 1])
        # Trim vector to current and last position
        j_pts.append(j_pt)

        if len(j_pts) < 2:
            j_pts.append(j_pt)
        if len(j_pts) > 2:
            j_pts = j_pts[1:]

        # Draw line between Jittered Points
        if count > 1:
            img = cv2.line(img, j_pts[0], j_pts[1], (128, 128, 128), 1, lineType=cv2.LINE_AA)

        # Draw Jittered Points
        img = cv2.circle(img, j_pt, 3, (128, 128, 128), -1, lineType=cv2.LINE_AA)

    # Reset loop
    if strength >= 1:
        change = -.1
    if strength <= .1:
        change = .1
        seeds = []

    # Show video
    cv2.imshow('Jitter', img)
    #cv2.imwrite("output/breadcrumbs_jitter/" + str(i) + "_s" + str(rng) + ".png", img)
    cv2.waitKey(1)



    strength += change
    #print(jitter)