import cv2

cap = cv2.VideoCapture(0)
i = 0

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    i += 1
    ret, frame = cap.read()
    cv2.imshow('Input', frame)
    cv2.imwrite("capture/" + str(i) + ".png", frame)
    c = cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
