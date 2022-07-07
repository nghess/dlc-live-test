import cv2
import numpy as np

width = 640
height = 480

image = np.zeros((height, width, 3), np.uint8)  # Clear frame
i = 0

def vf(x,y,i):
    vx = int(y + x**2 - i)
    vy = int(x + y**2 - i)
    vec = (vx, vy)
    return vec


while True:
    image = np.zeros((height, width, 3), np.uint8)  # Clear frame
    for x in range(0,width,20):
        for y in range(0, height, 20):
            vector = vf(x,y,i)
            print(vector)
            image = cv2.line(image, (x, y), vector, (0, 0, 255), 1)
    i += 5


    cv2.imshow('Vector Field', image)
    cv2.waitKey(1)