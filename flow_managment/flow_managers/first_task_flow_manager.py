from configuration.config import EYE_DETECTION_CASCADE_PATH, DETECTION_RECORDS_PATH, SAVE_FRAMES, CAMERA_PORT
from IO_operations.eyes_detection_record import append_detections_to_text_file
from flow_managment.task_flow_manager import TaskFlowManager
from generic.thread_helper import create_new_thread
import numpy as np
import time
import cv2

import sys
np.set_printoptions(threshold=sys.maxsize)  # needed for writing the full frame and not a truncated representation


class FirstTaskFlowManager(TaskFlowManager):

    def __init__(self):
        self._eye_cascade = cv2.CascadeClassifier(EYE_DETECTION_CASCADE_PATH)
        self._default_camera_port = CAMERA_PORT
        self._capture = cv2.VideoCapture(self._default_camera_port)
        self._transparency = 0.3
        self._frame_list: list[np.ndarray] = []

    def _get_eye_box_list(self, frame, scaleFactor=1.3, minNeighbors=5):
        # The following method returns the coordinates for every eye detected
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self._eye_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)

    def _brighten_detected_box(self, det_list, frame):
        overlay = frame.copy()
        for (x, y, w, h) in det_list:
            cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 255, 255), -1)
        frame = cv2.addWeighted(overlay, self._transparency, frame, 1 - self._transparency, 0)
        return frame

    @staticmethod
    def _detected(eyes):
        return len(eyes)

    def _write_frame_list_to_file(self):
        if SAVE_FRAMES:
            # append_detections_to_text_file(DETECTION_RECORDS_PATH, self._frame_list)  # no latency is allowed
            create_new_thread(append_detections_to_text_file, filepath=DETECTION_RECORDS_PATH, single_frame_dets=self._frame_list)

    def _analyze_live_feed(self):
        """
        The following method gets 'live' frames from the configured camera port.
        The eyes in each frame will be brighten

        * press 'q' to continue.
        ** FYI, SAVE_FRAME flag is True by default
        """
        while True:
            _, frame = self._capture.read()
            if frame is None:
                break
            eyes = self._get_eye_box_list(frame)
            if SAVE_FRAMES and self._detected(eyes):
                self._frame_list.append(frame.copy())
            frame = self._brighten_detected_box(eyes, frame)
            cv2.imshow('LiveVideo', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def flow(self):
        # todo: log for each step/ state
        self._analyze_live_feed()
        self._write_frame_list_to_file()
        self.clean_task()

    def clean_task(self):
        self._capture.release()
        cv2.destroyAllWindows()

# FirstTaskFlowManager().flow()
