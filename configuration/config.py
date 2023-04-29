import os

ROOT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
LOCAL_FILES_DIR = os.path.join(ROOT_PATH, 'local_files')

FIRST_TASK_OUTPUT_PATH = os.path.join(LOCAL_FILES_DIR, 'first_task_output')
CASCADES_PATH = os.path.join(LOCAL_FILES_DIR, 'cascades')
EYE_DETECTION_CASCADE_PATH = os.path.join(CASCADES_PATH, 'haarcascade_eye.xml')
DETECTION_RECORDS_PATH = os.path.join(CASCADES_PATH, r'C:\Users\ofir\Downloads\ttt.txt')  # todo

CAMERA_PORT = 1  # todo
SAVE_FRAMES = True  # todo
