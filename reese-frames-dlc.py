import cv2
import dlclive

i = 0

while True:
    i += 1
    cap = cv2.imread('output/ ('+str(i)+').png', 0)
    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', cap)
    #cv2.imwrite("output/" + str(i) + ".png", frame)
    c = cv2.waitKey(1)
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()