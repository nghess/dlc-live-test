import cv2
import numpy as np

height = 756
width = 756

origin = (int(height/2), int(width/2))

i = 0
count = 0


def orbit(dist, b1, spd=1):
    b2 = (b1[0]+dist, b1[1])
    c = (b2[0]-b1[0], b2[1] - b1[1])
    c = (int(c[0]*np.cos(i*spd) - c[1]*np.sin(i*spd)), int(c[0]*np.sin(i*spd) + c[1]*np.cos(i*spd)))
    c = (c[0]+b1[0], c[1]+b1[1])
    return c


while i <= 2*np.pi:

    i = i+.01

    m1 = orbit(200, origin)
    m2 = orbit(100, m1, 3)
    m3 = orbit(35, m2, 4)
    m4 = orbit(40, m2, 5)
    m5 = orbit(45, m2, 6)

    image = np.zeros((height, width, 3), np.uint8)  # Clear frame
    image = cv2.circle(image, origin, 50, (32, 16, 16), -1, lineType=cv2.LINE_AA)
    image = cv2.circle(image, m1, 15, (128, 75, 75), -1, lineType=cv2.LINE_AA)
    image = cv2.circle(image, m2, 7, (200, 128, 128), -1, lineType=cv2.LINE_AA)
    image = cv2.circle(image, m3, 1, (255, 255, 255), -1, lineType=cv2.LINE_AA)
    image = cv2.circle(image, m4, 1, (255, 255, 255), -1, lineType=cv2.LINE_AA)
    image = cv2.circle(image, m5, 1, (255, 255, 255), -1, lineType=cv2.LINE_AA)
    cv2.imshow('Points', image)

    count = count + 1
    cv2.imwrite("output/" + str(count) + ".png", image)
    cv2.waitKey(1)

