from configuration.config import EYE_DETECTION_CASCADE_PATH, DETECTION_RECORDS_PATH
from flow_managment.task_flow_manager import TaskFlowManager
# from generic.thread_helper import create_new_thread
import matplotlib.pyplot as plt
from typing import Union, Any
import pandas as pd
import numpy as np
import cv2


class SecondTaskFlowManager(TaskFlowManager):

    def __init__(self):
        self._eye_cascade = cv2.CascadeClassifier(EYE_DETECTION_CASCADE_PATH)
        self._angles_record: dict = {}
        self._frame_list: list[np.ndarray] = []

    def _dict_to_hist_plot(self, sort_by_key=True, color='g'):
        # clause C.
        ret_dict = self._angles_record
        if sort_by_key:
            keys = list(ret_dict.keys())
            keys.sort()
            ret_dict = {key: ret_dict.get(key) for key in keys}
        plt.bar(list(ret_dict.keys()), ret_dict.values(), color=color)
        plt.show()

    def _increment_dict_value(self, key: Union[int, str], default=0):
        self._angles_record[key] = self._angles_record.get(key, default) + 1

    def _get_frame_list_from_file(self, path='config_path'):
        # todo: from IO_operations import read file and set the list
        pass

    def _frame_list_filter(self):
        # Clause A.
        new_frame_list = []
        # todo
        return new_frame_list

    def _get_frames_df(self):
        pass

    def _get_eye_box_list(self, frame, scaleFactor=1.3, minNeighbors=5):
        """
        The following method returns the coordinates for every eye detected
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.eye_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)

    @staticmethod
    def _detected(eyes):
        return len(eyes)

    def _set_head_tilt_angle_list(self):
        """
        Inspired by https://www.geeksforgeeks.org/determine-the-face-tilt-using-opencv-python/
        """
        angle = 0
        for frame in self._frame_list:
            eyes = self._get_eye_box_list(frame)
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
                if delta_x:
                    angle = np.arctan(delta_y / delta_x)  # Slope of line formula
                    angle = int((angle * 180) / np.pi)  # Converting radians to degrees

            self._increment_dict_value(key=int(angle if angle else 0))

    def flow(self):
        # todo: log for each step/ state
        self._get_frame_list_from_file()
        self._frame_list_filter()
        self._set_head_tilt_angle_list()
        self._dict_to_hist_plot()
        self.clean_task()

    def clean_task(self):
        pass


# SecondTaskFlowManager().flow()

