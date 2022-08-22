import cv2
import numpy as np

width = 1024
height = 1024
origin = (int(width/2), int(height/2))

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


def rng():
    return np.random.randint(-.5*width, .5*height)

def rng_size(lo,hi):
    return np.random.randint(lo, hi)

def vf(x, y, length, norm=True, deg=True):
    x1 = x - origin[0]
    y1 = -y + origin[1]

    vx = y1/np.sin(x1**2 + y1**2)**2
    vy = x1/np.sqrt(x1**2 + y1**2)**2

    mag = np.linalg.norm([vx, vy])

    vec = [vx, vy]

    if norm is True:
        nv = vec/np.linalg.norm(vec)
        vec = (int(nv[0]*length+x), int(nv[1]*length+y))
    else:
        vec = (int(vec[0])+x1, int(vec[1])+y1)
    return vec, mag


change = 1
particle = (origin[0]+5, origin[1]+5)

image = np.zeros((height, width, 3), np.uint8)  # Clear frame
rad = 1

while True:


    vector1, m = vf(particle[0], particle[1], 2)
    image = cv2.circle(image, vector1, rad, (count-55, count-55, count+55), -1, lineType=cv2.LINE_AA)
    print(vector1)
    #frame = cv2.putText(image, str(int(d)), (u+1, v-2), cv2.FONT_HERSHEY_SIMPLEX, .2, (128, 128, 255*m))

    particle = vector1

    #New Particle
    if 1 > min(particle) or max(particle) > height:
        particle = (origin[0]+rng(), origin[1]+rng())
        rad = rng_size(1,10)

    count += change
    if count == 255:
        change = -1
    if count == 0:
        change = 1
    #cv2.imwrite("output/vf/" + str(count) + ".png", image)
    cv2.imshow('Vector Field', image)
    cv2.waitKey(1)
