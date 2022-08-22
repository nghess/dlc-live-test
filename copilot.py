import numpy as np
import cv2

height = 1024
width = 1024

image = np.zeros((height, width, 3), np.uint8)


#a differential equation solver
def euler(f, x, y, h):
    return x + h*f(x, y), y + h*f(x, y)


trajectory = []
x = 1
y = 5

while True:

    x, y = euler(lambda x, y: x*y, x, y, .1)
    print(x, y)

    trajectory.append((int(x), int(y)))

    if len(trajectory) > 1:
        for c in range(1, len(trajectory)):  # Draw lines between centers in trajectory list
            image = cv2.line(image, trajectory[c], trajectory[c-1], (0, 0, int((c/len(trajectory))*255), .01), 3, lineType=cv2.LINE_AA)

    cv2.imshow('image', image)
    cv2.waitKey(1)
#a = euler(lambda x, y: x, 0, 1, 0.1)

#print(a)