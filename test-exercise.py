from dlclive import DLCLive, Processor
from PIL import Image
from numpy import asarray
import time

folder = 'model/'
dlc_proc = Processor()
dlc_live = DLCLive(folder, processor=dlc_proc)

for i in range(0, 10):

    tic = time.perf_counter()
    img = Image.open('frames/mouse.tif')
    data = asarray(img)
    dlc_live.init_inference(data)
    pose = dlc_live.get_pose(data)
    toc = time.perf_counter()

    print(pose)
    print(f"{tic-toc:0.4f}")