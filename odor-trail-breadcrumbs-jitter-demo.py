import cv2
import numpy as np

# Initialize variables
change = 1   # Amount to change jitter by
jitter = 0  # Jitter for curve points
jit_ceil = 10
rng = 117  # Set random seed
np.random.seed(rng)

# Get video dimensions
frames_dir = "frames/breadcrumbs/"
arena = cv2.imread(frames_dir+' ('+str(1)+').png')
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

def angle_btw(u,v):
    nu = np.linalg.norm(u)
    nv = np.linalg.norm(v)
    theta = np.arccos(np.dot(u, v)/(nu*nv))

    theta = theta*(180/np.pi)
    return theta

# Curve points file
crv_file = "curves/arena_crv.txt"



while True:
    img = cv2.imread(frames_dir+' ('+str(1)+').png')
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    crv = load_curve(crv_file, jitter)

    # Draw curve
    for c in range(1, len(crv)):
        radius = 3
        color = (200, 200, 200)
        center_c = (int(crv[c][0]), int(crv[c][1]))
        center_p = (int(crv[c-1][0]), int(crv[c-1][1]))
        img = cv2.circle(img, center_c, radius, color, -1, lineType=cv2.LINE_AA)
        img = cv2.line(img, center_c, center_p, color, 1, lineType=cv2.LINE_AA)

    for c in range(12, 15):

        center_c = (int(crv[c][0]), int(crv[c][1]))
        center_p = (int(crv[c-1][0]), int(crv[c-1][1]))


        # Draw normals
        u = center_c
        v = [center_c[0], center_c[1]-50]

        pt1 = v
        pt2 = center_p

        u = np.subtract(pt1, center_c)
        v = np.subtract(pt2, center_c)

        print(u, v)
        rad = angle_btw(u, v)
        #print(rad)

        img = cv2.circle(img, center_c, 3, (255,255,0), -1, lineType=cv2.LINE_AA)
        img = cv2.circle(img, pt1, 3, (0,255,0), -1, lineType=cv2.LINE_AA)
        img = cv2.circle(img, pt2, 3, (0,128,128), -1, lineType=cv2.LINE_AA)
        normal = orbit(cv2.norm(pt2, center_c), center_c, 30/(180/np.pi))

        img = cv2.circle(img, normal, 3, (0,128,128), -1, lineType=cv2.LINE_AA)

        img = cv2.line(img, np.add(u, center_c), np.add(v, center_c), (0, 0, 255), 1, lineType=cv2.LINE_AA)
        img = cv2.line(img, center_c, center_p, (255, 0, 0), 1, lineType=cv2.LINE_AA)
        #img = cv2.line(img, np.add(normal, origin), center_p, color, 1, lineType=cv2.LINE_AA)

        img = cv2.putText(img, str(int(rad*(180/np.pi))), (center_p[0]+10, center_p[1]+10), cv2.FONT_HERSHEY_SIMPLEX, .25, (0, 0, 0))
    # Show video
    cv2.imshow('Jitter', img)
    #cv2.imwrite("output/breadcrumbs_jitter/" + str(i) + "_s" + str(rng) + ".png", frame)
    cv2.waitKey(16)

    # Reset loop
    if jitter >= jit_ceil:
        change = -.01
    if jitter <= .1:
        change = .01

    jitter += 0
    #print(jitter)