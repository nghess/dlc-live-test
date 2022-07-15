import cv2
import numpy as np

width = 1920
height = 1080

image = np.zeros((height, width, 3), np.uint8)  # Clear frame
i = 0
count = 0


def rotate(x, y, d):
    rot = (int(x * np.cos(d) - y * np.sin(d)), int(x * np.sin(d) + y * np.cos(d)))
    return rot


def angle_btw(u,v):
    nu = np.linalg.norm(u)
    nv = np.linalg.norm(v)
    theta = np.arccos(np.dot(u, v)/(nu*nv))
    theta = theta*(180/np.pi)
    return theta


def vf(x, y, length, d, norm=True, deg=True):
    vx = -y/np.sqrt(x + y)
    vy = x/np.sqrt(x + y)
    mag = cv2.norm((x, y), (vx, vy))*.001
    rot = rotate(vx, vy, d)
    vec = [rot[0], rot[1]]

    if deg is True:
        degree = angle_btw(vec, [0, 10])

    if norm is True:
        nv = vec/np.linalg.norm(vec)
        vec = (int(nv[0]*length+x), int(nv[1]*length+y))
    else:
        vec = [int(rot[0])+x, int(rot[1])+y]

    return vec, mag, degree


while True:
    image = np.zeros((height, width, 3), np.uint8)  # Clear frame
    for u in range(10, width, 20):
        for v in range(10, height, 20):
            vector, m, d = vf(u, v, 10, i, norm=True)
            image = cv2.line(image, (u, v), vector, (128, 128, 255*m), 1, lineType=cv2.LINE_AA)
            image = cv2.circle(image, vector, 1, (128, 128, 255*m), -1, lineType=cv2.LINE_AA)
            frame = cv2.putText(image, str(int(d)), (u+1, v-2), cv2.FONT_HERSHEY_SIMPLEX, .2, (128, 128, 255*m))

    count += 1
    cv2.imwrite("output/vf/" + str(count) + ".png", image)
    cv2.imshow('Vector Field', image)
    cv2.waitKey(10000)
    #i += .1

    if i >= 2*np.pi:
        #i = 0
        break
