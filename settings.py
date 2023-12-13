from easydict import EasyDict as edict

__APP_SETTINGS__ = edict()

# Number of frames to pass before changing the frame to compare the current
# frame against
__APP_SETTINGS__.FRAMES_TO_PERSIST = 1

# Minimum boxed area for a detected motion to count as actual motion
# Use to filter out noise or small objects
__APP_SETTINGS__.MIN_SIZE_FOR_MOVEMENT = 3

# Minimum length of time where no motion is detected it should take
#(in program cycles) for the program to declare that there is no movement
__APP_SETTINGS__.MOVEMENT_DETECTED_PERSISTENCE = 20