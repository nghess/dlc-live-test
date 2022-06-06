import cv2
from dlclive import DLCLive, Processor

folder = 'model/'
dlc_proc = Processor()
dlc_live = DLCLive(folder, processor=dlc_proc)
dlc_live.init_inference()

i = 0
radius = 5
thickness = -1

while True:
    i += 1
    frame = cv2.imread('frames/ ('+str(i)+').jpg')
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    pose = dlc_live.get_pose(frame)

    c0 = (int(pose[0, 0]), int(pose[0, 1]))
    c1 = (int(pose[1, 0]), int(pose[1, 1]))
    c2 = (int(pose[2, 0]), int(pose[2, 1]))
    target = (int(frame.shape[1]-5), int(frame.shape[0]/2))
    distance = tuple(map(lambda k, v: abs(k - v), target, c0))
    x = round((target[1]-distance[1])/target[1], 2)
    y = round((target[0]-distance[0])/target[0], 2)
    pct = x*y
    #print(pct)

    frame = cv2.circle(frame, c0, radius, (int(255*pct), int(255*pct), 0), thickness)
    #frame = cv2.circle(frame, c1, radius, (0, 255, 0), thickness)
    #frame = cv2.circle(frame, c2, radius, (0, 0, 255), thickness)
    #frame = cv2.circle(frame, target, radius, (0, 128, 255), thickness)

    cv2.imshow('Pose', frame)

    #cv2.imwrite("output/" + str(i) + ".png", frame)

    cv2.waitKey(1)
    if i == 999:
        i = 0

#cap.release()
#cv2.destroyAllWindows()