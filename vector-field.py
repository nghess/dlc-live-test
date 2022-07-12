import cv2
import numpy as np

width = 640
height = 480

image = np.zeros((height, width, 3), np.uint8)  # Clear frame
i = 0


def vf(x, y, length):
    vx = -y/np.sqrt(x + y)
    vy = x/np.sqrt(x + y)
    mag = cv2.norm((x, y), (vx, vy))*.001
    vec = [vx, vy]
    nv = vec/np.linalg.norm(vec)
    vec = (int(nv[0]*length+x), int(nv[1]*length+y))
    return vec, mag

def vf2(x, y, length):
    vx = -y/np.sqrt(x + y)
    vy = x/np.sqrt(x + y)
    mag = np.sqrt(vx**2+vy**2)
    uni = (vx/mag, vy/mag)
    vec = (x-int((vx*uni[0])*length), y-int((vy*uni[1])*length)+y)
    return vec, mag


while True:
    image = np.zeros((height, width, 3), np.uint8)  # Clear frame
    for u in range(1, width, 20):
        for v in range(1, height, 20):
            vector, m = vf(u, v, 10)
            image = cv2.line(image, (u, v), vector, (128, 128, 255*m), 1, lineType=cv2.LINE_AA)
            image = cv2.circle(image, vector, 1, (128, 128, 255*m), -1, lineType=cv2.LINE_AA)

    cv2.imshow('Vector Field', image)
    cv2.waitKey(1)
