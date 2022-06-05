from dlclive import DLCLive, Processor
from PIL import Image
from numpy import asarray

img = Image.open('frames/mouse.tif')

data = asarray(img)
folder = 'model/'

print(data.ndim)

dlc_proc = Processor()
dlc_live = DLCLive(folder, processor=dlc_proc)
dlc_live.init_inference(data)
pose = dlc_live.get_pose(data)

print(pose)