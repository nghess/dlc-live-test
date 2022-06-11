import cv2
import numpy as np

height = 756
width = 756

origin = (int(height/2), int(width/2))
length = (int(height/2), int(width/10))
degree = 0
change = 1


def orbit(point1, point0, degrees):
    deg = degrees*(np.pi/180)
    c = (point1[0]-point0[0], point1[1] - point0[1])
    c = (int(c[0]*np.cos(deg) - c[1]*np.sin(deg)), int(c[0]*np.sin(deg) + c[1]*np.cos(deg)))
    c = (c[0]+point0[0], c[1]+point0[1])
    return c


while True:
    degree = degree + 1

    p1 = orbit(length, origin, degree)
    p2 = orbit(length, origin, -degree)
    axes = (origin[1]-length[1], origin[1]-length[1])

    image = np.zeros((height, width, 3), np.uint8)  # Clear frame

    image = cv2.line(image, p1, origin, (255, 255, 0), 1)
    image = cv2.circle(image, p1, 5, (0, 255, 255), 1)
    image = cv2.line(image, p2, origin, (255, 255, 0), 1)
    image = cv2.circle(image, p2, 5, (0, 255, 255), 1)
    image = cv2.ellipse(image, origin, axes, -90, -degree, degree, (0, 0, 255))

    print(p1)
    print(origin)
    print(axes)

    cv2.imshow('Cone', image)
    cv2.waitKey(16)
    if degree == 180:
        degree = -180
        change = -1
    if degree == 0:
        change = 1
