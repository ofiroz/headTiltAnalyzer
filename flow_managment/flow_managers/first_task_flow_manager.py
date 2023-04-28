from configuration.config import EYE_DETECTION_CASCADE_PATH, DETECTION_RECORDS_PATH, SAVE_FRAMES, CAMERA_PORT
from IO_operations.eyes_detection_record import append_detections_to_text_file
from flow_managment.task_flow_manager import TaskFlowManager
from generic.thread_helper import create_new_thread
import numpy as np
import time
import cv2


class FirstTaskFlowManager(TaskFlowManager):

    def __init__(self):
        self.eye_cascade = cv2.CascadeClassifier(EYE_DETECTION_CASCADE_PATH)
        self.default_camera_port = CAMERA_PORT
        self.capture = cv2.VideoCapture(self.default_camera_port)
        self.transparency = 0.2
        self.frame_list: list[np.ndarray] = []

    def _get_eye_box_list(self, frame, scaleFactor=1.3, minNeighbors=5):
        # The following method returns the coordinates for every eye detected
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.eye_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)

    def _brighten_detected_box(self, det_list, frame):
        overlay = frame.copy()
        for (x, y, w, h) in det_list:
            cv2.rectangle(overlay, (x, y), (x + w, y + h), (255, 255, 255), -1)
        return overlay

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
        while True:
            _, frame = self.capture.read()
            eyes = self._get_eye_box_list(frame)
            if SAVE_FRAMES and self._detected(eyes):
                self.frame_list.append(frame)
                # TODO: EXTRACT 1 FRAME (~10TH) AND SAVE ONLY IT (OVERRIDE FRAME_LIST). THEN FIND THE DETECTION FLAG
            overlay = self._brighten_detected_box(eyes, frame)
            frame = cv2.addWeighted(overlay, self.transparency, frame, 1 - self.transparency, 0)
            cv2.imshow('LiveVideo', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                if SAVE_FRAMES:
                    # append_detections_to_text_file(r'C:\Users\ofir\Downloads\ttt.txt', self.frame_list)
                    create_new_thread(append_detections_to_text_file, filepath=r'C:\Users\ofir\Downloads\ttt.txt', single_frame_dets=self.frame_list)
                break

    def flow(self):
        # todo: log
        self._analyze_live_feed()
        self.clean_task()
        # todo: log

    def clean_task(self):
        self.capture.release()
        cv2.destroyAllWindows()

FirstTaskFlowManager().flow()