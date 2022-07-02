import deeplabcut

# Getting multithreading error in pycharm. Works in ubuntu.

ProjectFolderName = '//wsl$/Ubuntu-20.04/home/nghess/Hand Test-NG Hess-2022-06-30'
VideoType = 'mp4'

# Set paths
videofile_path = [ProjectFolderName+'/videos']
path_config_file = ProjectFolderName+'/config.yaml'

deeplabcut.export_model(path_config_file, iteration=None, shuffle=1, trainingsetindex=0, snapshotindex=None, TFGPUinference=True, overwrite=False, make_tar=False)
