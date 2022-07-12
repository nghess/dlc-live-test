import numpy as np
import cv2

i = 0

while True:
    # Load frame
    i += 1
    frame1 = cv2.imread('frames/ (' + str(i) + ').jpg')
    frame1 = cv2.resize(frame1, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)
    frame2 = cv2.imread('frames/ (' + str(i + 2) + ').jpg')
    frame2 = cv2.resize(frame2, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_AREA)

    frame1 = cv2.GaussianBlur(frame1, (15, 15), cv2.BORDER_DEFAULT)
    ret, thresh1 = cv2.threshold(frame1, 48, 255, 0)

    frame2 = cv2.GaussianBlur(frame2, (15, 15), cv2.BORDER_DEFAULT)
    ret, thresh2 = cv2.threshold(frame2, 48, 255, 0)

    prvs = cv2.cvtColor(thresh1, cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    next = cv2.cvtColor(thresh2, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prvs, next, None, 0.5, 1, 3, 5, 3, 1.1, 0)
    mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv[..., 0] = ang*180/np.pi/2
    hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    ret, thresh3 = cv2.threshold(bgr, 1, 255, 0)

    cv2.imshow('frame2', thresh3)
    k = cv2.waitKey(1) & 0xff

    prvs = next

cv2.destroyAllWindows()