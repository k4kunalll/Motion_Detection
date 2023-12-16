from easydict import EasyDict as edict

__APP_SETTINGS__ = edict()

__APP_SETTINGS__.RTSP_LINK = "videos/Demo6.mp4"

__APP_SETTINGS__.DOTS_HISTORY = 200

__APP_SETTINGS__.ROI_XY_MIN = (640,200)
__APP_SETTINGS__.ROI_XY_MAX = (1793,969)

__APP_SETTINGS__.VIDEO_FPS = 20
__APP_SETTINGS__.VIDEO_PATH = 'generated_videos'

__APP_SETTINGS__.VIDEO_SAVE_FRAMES_THRESH = 50

__APP_SETTINGS__.FRAMES_TO_PERSIST = 1

__APP_SETTINGS__.EXCEL_DIR = 'report_excel'

__APP_SETTINGS__.EXCEL_NAME = 'Data.csv'

__APP_SETTINGS__.BLUR_KERNEL = (21, 21)
__APP_SETTINGS__.DILATION_KERNEL = (10, 255)

__APP_SETTINGS__.MIN_MIX_DIST = (10,25)


