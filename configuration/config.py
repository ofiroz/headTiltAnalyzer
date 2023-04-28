import os

ROOT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
LOCAL_FILES_DIR = os.path.join(ROOT_PATH, 'local_files')

FIRST_TASK_OUTPUT_PATH = os.path.join(LOCAL_FILES_DIR, 'first_task_output')
CASCADES_PATH = os.path.join(LOCAL_FILES_DIR, 'cascades')
EYE_DETECTION_CASCADE_PATH = os.path.join(CASCADES_PATH, 'haarcascade_eye.xml')
DETECTION_RECORDS_PATH = os.path.join(CASCADES_PATH, 'haarcascade_eye.xml')

# import numpy as np
# import cv2
#
# eyeCascade = cv2.CascadeClassifier(EYE_DETECTION_CASCADE)
#
# video_capture = cv2.VideoCapture(1)
#
# while True:
#     # Capture frame-by-frame
#     ret, frame = video_capture.read()
#
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#     eyes = eyeCascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
#
#     overlay = frame.copy()
#
#     # Draw a rectangle around the faces
#     for (x, y, w, h) in eyes:
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
#         cv2.rectangle(overlay, (x, y), (x + w, y + h), (0, 200, 0), -1)
#     alpha = 0.4
#     frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
#
#
#     # Display the resulting frame
#     cv2.imshow('LiveVideo', frame)
#
#     if cv2.waitKey(1) & 0xFF == ord('x'):  # todo: p
#         break
#
# # When everything is done, release the capture
# video_capture.release()
# cv2.destroyAllWindows()