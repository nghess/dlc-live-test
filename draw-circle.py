import cv2
import numpy as np

height = 756
width = 756
degree = 0

origin = (int(height/2), int(width/2))
length = (int(height/2), int(width/10))


def angle_btw(u,v):
    nu = np.linalg.norm(u)
    nv = np.linalg.norm(v)
    theta = np.arccos(np.dot(u, v)/(nu*nv))
    theta = theta*(180/np.pi)
    return theta


def orbit(point1, point0, degrees):
    deg = degrees*(np.pi/180)
    c = (point1[0]-point0[0], point1[1] - point0[1])
    c = (int(c[0]*np.cos(deg) - c[1]*np.sin(deg)), int(c[0]*np.sin(deg) + c[1]*np.cos(deg)))
    c = (c[0]+point0[0], c[1]+point0[1])
    return c


rand_vec = np.random.randint(1, 359)
angle_dif = ''

while True:
    degree = degree + 1

    p1 = orbit(length, origin, degree)
    axes = (origin[1]-length[1], origin[1]-length[1])

    # Measure arbitrary angle
    ref_vec = orbit(length, origin, rand_vec)
    u = np.subtract(p1, origin)
    v = np.subtract(ref_vec, origin)
    if u[0] != v[0]:
        print(u, v)
        angle_dif = int(angle_btw(u, v))

    # Clear frame
    image = np.zeros((height, width, 3), np.uint8)

    # Draw Contours
    image = cv2.line(image, p1, origin, (0, 0, 255), 1)
    image = cv2.line(image, length, origin, (0, 0, 255), 1)
    image = cv2.ellipse(image, origin, axes, -90, 0, degree, (0, 0, 255))

    # Fill Layer
    contour = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contour = cv2.findContours(contour, mode=1, method=1)
    image = cv2.drawContours(image, [contour[0][0]], -1, color=(0, 0, abs(degree)), thickness=-1, lineType=cv2.LINE_AA)

    # Final Layer
    image = cv2.circle(image, length, 5, (255, 255, 255), -1, lineType=cv2.LINE_AA)
    image = cv2.circle(image, p1, 5, (255, 255, 255), -1, lineType=cv2.LINE_AA)
    image = cv2.ellipse(image, origin, axes, -90, 0, degree, (255, 255, 255), lineType=cv2.LINE_AA)
    image = cv2.line(image, p1, origin, (255, 255, 255), 1, lineType=cv2.LINE_AA)
    image = cv2.line(image, length, origin, (255, 255, 255), 1, lineType=cv2.LINE_AA)
    image = cv2.line(image, ref_vec, origin, (255, 255, 0), 1, lineType=cv2.LINE_AA)  # Random vector to reference

    frame = cv2.putText(image, str(degree), (p1[0]-50, p1[1]+50), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255))
    frame = cv2.putText(image, str(angle_dif), (ref_vec[0]-50, ref_vec[1]+50), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255))

    frame = cv2.putText(image, f'{p1}', (p1[0]+10, p1[1]-10), cv2.FONT_HERSHEY_SIMPLEX, .3, (255, 255, 0))
    frame = cv2.putText(image, f'{ref_vec}', (ref_vec[0]+10, ref_vec[1]-10), cv2.FONT_HERSHEY_SIMPLEX, .3, (255, 255, 0))

    cv2.imshow('Cone', image)
    cv2.waitKey(10)
    if degree >= 360:
        degree = 1
        rand_vec = np.random.randint(0, 359)
