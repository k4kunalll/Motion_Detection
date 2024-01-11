from easydict import EasyDict as edict

__APP_SETTINGS__ = edict()

__APP_SETTINGS__.RTSP_LINK = "videos/Demo.mp4"

__APP_SETTINGS__.DOTS_HISTORY = 200

__APP_SETTINGS__.POLY_COOR = [
            [844, 182],
            [1092, 230],
            [1448, 514],
            [1448, 942],
            [684, 942],
            [696, 338],
            [840, 186],
        ]

__APP_SETTINGS__.VIDEO_FPS = 30
__APP_SETTINGS__.VIDEO_PATH = "generated_videos"

#Number of frames to pass before changing the frame to compare the current frame
__APP_SETTINGS__.FRAMES_TO_PERSIST = 10

__APP_SETTINGS__.EXCEL_DIR = "report_excel"

__APP_SETTINGS__.EXCEL_NAME = "Data.csv"

__APP_SETTINGS__.BLUR_KERNEL = (39, 39)
__APP_SETTINGS__.DILATION_KERNEL = (20, 255)

__APP_SETTINGS__.MIN_MIX_DIST = (0, 100)

__APP_SETTINGS__.MOVEMENT_DETECTED_PERSISTENCE = 50

__APP_SETTINGS__.FRAMESAVE_THRESH = 50