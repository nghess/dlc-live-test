from dlclive import DLCLive, Processor

frame = test_frame
dir = '/model/'

dlc_proc = Processor()
dlc_live = DLCLive(dir, processor=dlc_proc)
dlc_live.init_inference(frame)
print(dlc_live.get_pose(frame))