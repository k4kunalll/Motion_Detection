from easydict import EasyDict as edict

__APP_SETTINGS__ = edict()

__APP_SETTINGS__.RTSP_LINK = "videos/Demo.mp4"

__APP_SETTINGS__.DOTS_HISTORY = 200

__APP_SETTINGS__.ROI_XY_MIN = (693, 252)
__APP_SETTINGS__.ROI_XY_MAX = (1662, 879)

__APP_SETTINGS__.VIDEO_FPS = 30
__APP_SETTINGS__.VIDEO_PATH = "generated_videos"

__APP_SETTINGS__.VIDEO_SAVE_FRAMES_THRESH = 80

__APP_SETTINGS__.FRAMES_TO_PERSIST = 1

__APP_SETTINGS__.EXCEL_DIR = "report_excel"

__APP_SETTINGS__.EXCEL_NAME = "Data.csv"

__APP_SETTINGS__.BLUR_KERNEL = (31, 31)
__APP_SETTINGS__.DILATION_KERNEL = (20, 255)

__APP_SETTINGS__.MIN_MIX_DIST = (5, 25)
