import cv2
import numpy as np

width = 1920
height = 1080
origin = (int(width/2), int(height/2))

image = np.zeros((height, width, 3), np.uint8)  # Clear frame


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
    x1 = x - origin[0]
    y1 = -y + origin[1]

    vx = y1/np.sqrt(x1**2 + y1**2)
    vy = x1/np.sqrt(x1**2 + y1**2)

    mag = np.linalg.norm([vx, vy])

    vec = [vx, vy]
    if deg is True:
        degree = angle_btw(vec, [0, 10])

    if norm is True:
        nv = vec/np.linalg.norm(vec)
        vec = (int(nv[0]*length+x), int(nv[1]*length+y))
    else:
        vec = (int(vec[0])+x1, int(vec[1])+y1)
    return vec, mag, degree


def vf_gen(save=False, show=False):
    i = 0
    count = 0
    while True:
        image = np.zeros((height, width, 3), np.uint8)  # Clear frame
        for u in range(10, width, 20):
            for v in range(10, height, 20):
                vector, m, d = vf(u, v, 10, i, norm=True)
                image = cv2.line(image, (u, v), vector, (128, 128, 255*m), 1, lineType=cv2.LINE_AA)
                image = cv2.circle(image, vector, 1, (128, 128, 255*m), -1, lineType=cv2.LINE_AA)
                #frame = cv2.putText(image, str(int(d)), (u+1, v-2), cv2.FONT_HERSHEY_SIMPLEX, .2, (128, 128, 255*m))

        count += 1

        if save:
            cv2.imwrite("output/vf/" + str(count) + ".png", image)
        if show:
            cv2.imshow('Vector Field', image)
            cv2.waitKey(10000)

        if i >= 2*np.pi:
            i = 0
            break