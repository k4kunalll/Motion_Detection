from utils.motion import motion
from settings import __APP_SETTINGS__


if __name__ == "__main__":
    motion(__APP_SETTINGS__.RTSP_LINK)
