import time
import cv2
from dlclive import DLCLive, Processor

folder = 'model/'
dlc_proc = Processor()
dlc_live = DLCLive(folder, processor=dlc_proc)
dlc_live.init_inference()

f_times = []

for i in range(1, 11):

    tic = time.perf_counter()
    img = cv2.imread('frames/ ('+str(i)+').jpg', 0)
    #data = asarray(img)

    pose = dlc_live.get_pose(img)
    toc = time.perf_counter()

    print(img.shape[1])
    #print(f"{tic-toc:0.4f}")
    f_times.append(f"{tic-toc:0.4f}")

print(f_times)