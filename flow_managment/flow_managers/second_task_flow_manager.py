from configuration.config import EYE_DETECTION_CASCADE_PATH, DETECTION_RECORDS_PATH, SAVE_FRAMES, CAMERA_PORT
# from IO_operations.eyes_detection_record import append_detections_to_text_file
from flow_managment.task_flow_manager import TaskFlowManager
# from generic.thread_helper import create_new_thread
import pandas as pd
import numpy as np
# import time
import matplotlib.pyplot as plt
from typing import Union, Any
import cv2


class SecondTaskFlowManager(TaskFlowManager):

    def __init__(self):
        self._angles_record: dict = {}



        self.eye_cascade = cv2.CascadeClassifier(EYE_DETECTION_CASCADE_PATH)
        self.default_camera_port = CAMERA_PORT
        self.capture = cv2.VideoCapture(self.default_camera_port)
        self.transparency = 0.3
        self.frame_list: list[np.ndarray] = []

    def _dict_to_hist_plot(self, sort_by_key=True, color='g'):
        # C.
        ret_dict = self._angles_record
        if sort_by_key:
            keys = list(ret_dict.keys())
            keys.sort()
            ret_dict = {key: ret_dict.get(key) for key in keys}
        plt.bar(list(ret_dict.keys()), ret_dict.values(), color=color)
        plt.show()

    def _increment_dict_value(self, key: Union[int, str], default=0):
        self._angles_record[key] = self._angles_record.get(key, default) + 1




    def _get_frames_df(self):
        pass

    def _get_eye_box_list(self, frame, scaleFactor=1.3, minNeighbors=5):
        # The following method returns the coordinates for every eye detected
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.eye_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)

    @staticmethod
    def _detected(eyes):
        return len(eyes)

    def _analyze_live_feed(self):
        """
        The following method gets 'live' frames from the configured camera port.
        The eyes in each frame will be brighten and every detection will be recorded using append_detections_to_text_file function

        * press 'q' to continue.
        ** FYI, SAVE_FRAME flag is True by default todo
        """
        # referenced from https://www.geeksforgeeks.org/determine-the-face-tilt-using-opencv-python/
        angle = None
        while True:
            _, frame = self.capture.read()
            eyes = self._get_eye_box_list(frame)
            # todo
            x, y, w, h = 0, 0, 0, 0
            index = 0
            eye_1 = [None] * 4
            eye_2 = [None] * 4
            for (ex, ey, ew, eh) in eyes:
                if index == 0:
                    eye_1 = [ex, ey, ew, eh]
                elif index == 1:
                    eye_2 = [ex, ey, ew, eh]
                cv2.rectangle(frame[y:(y + h), x:(x + w)], (ex, ey),
                              (ex + ew, ey + eh), (0, 0, 255), 2)
                index = index + 1
            if (eye_1[0] is not None) and (eye_2[0] is not None):
                if eye_1[0] < eye_2[0]:
                    left_eye = eye_1
                    right_eye = eye_2
                else:
                    left_eye = eye_2
                    right_eye = eye_1
                left_eye_center = (
                    int(left_eye[0] + (left_eye[2] / 2)),
                    int(left_eye[1] + (left_eye[3] / 2)))

                right_eye_center = (
                    int(right_eye[0] + (right_eye[2] / 2)),
                    int(right_eye[1] + (right_eye[3] / 2)))

                left_eye_x = left_eye_center[0]
                left_eye_y = left_eye_center[1]
                right_eye_x = right_eye_center[0]
                right_eye_y = right_eye_center[1]

                delta_x = right_eye_x - left_eye_x
                delta_y = right_eye_y - left_eye_y

                # Slope of line formula todo: make sure x!=0
                angle = np.arctan(delta_y / delta_x)

                # Converting radians to degrees
                angle = (angle * 180) / np.pi

                # Provided a margin of error of 10 degrees
                # (i.e, if the face tilts more than 10 degrees
                # on either side the program will classify as right or left tilt)
                if angle > 10:
                    cv2.putText(frame, 'RIGHT TILT :' + str(int(angle)) + ' degrees',
                                (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 0), 2, cv2.LINE_4)
                elif angle < -10:
                    cv2.putText(frame, 'LEFT TILT :' + str(int(angle)) + ' degrees',
                                (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 0), 2, cv2.LINE_4)
                else:
                    cv2.putText(frame, 'STRAIGHT :', (20, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 0, 0), 2, cv2.LINE_4)
            # todo

            cv2.imshow('LiveVideo', frame)
            self._increment_dict_value(key=int(angle if angle else 0))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                p=0

    def flow(self):
        # todo: log
        self._analyze_live_feed()
        self.clean_task()
        # todo: log

    def clean_task(self):
        self.capture.release()
        cv2.destroyAllWindows()


SecondTaskFlowManager().flow()

import matplotlib.pyplot as plt
dictionary = {1: 27, 34: 1, 3: 72, 4: 62, 5: 33, 6: 36, 7: 20, 8: 12, 9: 9, 10: 6, 11: 5,
              12: 8, 2: 74, 14: 4, 15: 3, 16: 1, 17: 1, 18: 1, 19: 1, 21: 1, 27: 2}
plt.bar(list(dictionary.keys()), dictionary.values(), color='g')
plt.show()
# nd = np.array([[11,22,33],[44,55,66]])
#
# p=0
# with open(DETECTION_RECORDS_PATH) as f:
#     lines = f.readlines()
# lines[0] = lines[0].split('\t')[-1]
# p=0
