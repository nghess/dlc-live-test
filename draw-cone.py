import cv2
import numpy as np

height = 756
width = 756
origin = (int(height/2), int(width/3))
p1 = (int(height/3), int(width/3))

image = np.zeros((height, width, 3), np.uint8)  # Clear frame

image = cv2.line(image, origin, p1, (255, 255, 0), 1)
