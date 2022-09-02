import cv2
import numpy as np


def load_curve(crv_file):
    file = open(crv_file, "r")
    data = file.read()
    # Formatting as list
    crv_pts = data.replace('{', '[').replace('}', ']').split('\n')
    # Convert each point to a list within the main list
    for p in range(len(crv_pts)):
        crv_pts[p] = eval(crv_pts[p])
    return crv_pts

# Function to loop at the end of a list
def list_looper(i, chunk, list):
    neg = i-chunk-1
    stub = list[i-1::-1] + list[:neg:-1]
    return stub

# Define canvas
height = 756
width = 756
degree = 0
offset = (int(height/2), int(width/2))
# Curve points file
crv_file = "infinity_1k.txt"

full_crv = load_curve(crv_file)
i = 0
trail = int((len(full_crv)-1)/6)
crv = []

while True:
    i += 1
    if i > trail:
        crv = full_crv[i:i-trail:-1]
    elif i <= trail:
        crv = list_looper(i, trail, full_crv)
    image = np.zeros((height, width, 3), np.uint8)  # Clear frame
    for c in reversed(range(len(crv))):
        color = (255-(int((c/len(crv))*255)+10), 255-(int((c/len(crv))*255)+10), 0)
        #color = (255, 255, 255)
        radius = 10-int((c/len(crv))*10)+1
        center_c = (int(crv[c][0]+offset[0]), int(crv[c][1]+offset[1]))
        #center_p = (int(crv[c-1][0])+offset[0], int(crv[c-1][1])+offset[1])
        image = cv2.circle(image, center_c, radius, color, -1, lineType=cv2.LINE_AA)

    cv2.imwrite("output/looping_path/" + str(i) + ".png", frame)
    cv2.imshow('Points', image)
    cv2.waitKey(1)


    if i == len(full_crv):
        i = 0
