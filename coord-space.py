import numpy as np
import cv2

# Set up canvas
width = 1024
height = 1024
origin = (int(height/2), int(width/2))

# Clear frame
image = np.zeros((height, width, 3), np.uint8)

for u in range(10, width, 48):
    for v in range(10, height, 48):
        image = cv2.circle(image, (u, v), 1, (255, 255, 255), -1, lineType=cv2.LINE_AA)
        frame = cv2.putText(image, f'({u-origin[0]}, {-v+origin[1]})', (u+2, v-2), cv2.FONT_HERSHEY_SIMPLEX, .2, (255, 255, 0))

cv2.imshow('Coord Space', image)
cv2.waitKey(100000)