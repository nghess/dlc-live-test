import numpy as np
import cv2

height = 756
width = 756
origin = [int(height/2), int(width/2)]


def mag(x):
    return np.sqrt(sum(i**2 for i in x))


def angle_btw(u,v):
    nu = np.linalg.norm(u)
    nv = np.linalg.norm(v)
    theta = np.arccos(np.dot(u, v)/(nu*nv))
    theta = theta*(180/np.pi)
    return theta


u = [127, 209]
v = [680, 389]

u = np.subtract(u, origin)
v = np.subtract(v, origin)

angle = angle_btw(u, v)

while True:
    # Clear frame
    image = np.zeros((height, width, 3), np.uint8)

    # Draw Vectors
    image = cv2.line(image, np.add(u, origin), origin, (0, 0, 255), 1)
    image = cv2.line(image, np.add(v, origin), origin, (255, 255, 0), 1)

    frame = cv2.putText(image, str(angle), (origin[0]-50, origin[1]+50), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255))

    cv2.imshow('Angle Between Vectors', image)
    cv2.waitKey(1)


