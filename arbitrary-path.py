import cv2
import numpy as np


def load_curve(crv_file):
    file = open(crv_file, "r")
    data = file.read()
    # Formatting as list
    crv_pts = data.replace('{', '[').replace('}', ']').split('\n')
    # converting to list of lists
    for p in range(len(crv_pts)):
        crv_pts[p] = eval(crv_pts[p])
    return crv_pts


# Curve points file
crv_file = "curves/infinity.txt"
# Define canvas
height = 1080
width = 1080
degree = 0
offset = (int(height/2), int(width/2))
i = 0


while True:
    i += 1
    image = np.zeros((height, width, 3), np.uint8)  # Clear frame
    crv = load_curve(crv_file)
    for c in range(len(crv)):
        color = (int((c/len(crv))*255)+50, int((c/len(crv))*255)+50, 0)
        center_c = (int(crv[c][0])+offset[0], int(crv[c][1])+offset[1])
        center_p = (int(crv[c-1][0])+offset[0], int(crv[c-1][1])+offset[1])
        image = cv2.line(image, center_c, center_p, color, 1, lineType=cv2.LINE_AA)
        image = cv2.circle(image, center_c, 5, color, -1, lineType=cv2.LINE_AA)
        #image = cv2.putText(image, str(c), center_c, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

    cv2.imshow('Points', image)
    cv2.imwrite("output/segmentation/" + str(i) + ".png", image)
    cv2.waitKey(100)
