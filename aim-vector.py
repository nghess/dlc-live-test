import numpy as np
import cv2

vector = np.asarray([[x, 0] for x in range(20)])

print(vector[3])

aim = [1, 1]

aimed = np.dot(vector, aim)

print(aimed)