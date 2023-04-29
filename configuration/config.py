import os

ROOT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
LOCAL_FILES_DIR = os.path.join(ROOT_PATH, 'local_files')

CASCADES_PATH = os.path.join(LOCAL_FILES_DIR, 'cascades')
EYE_DETECTION_CASCADE_PATH = os.path.join(CASCADES_PATH, 'haarcascade_eye.xml')
DETECTION_RECORDS_PATH = os.path.join(LOCAL_FILES_DIR, 'first_task_output', 'output.txt')

CAMERA_PORT = 1  # todo: default is 0
CAMERA_PORT = r'C:\Users\ofir\Downloads\sw_eng_interview_input.avi'
SAVE_FRAMES = True
