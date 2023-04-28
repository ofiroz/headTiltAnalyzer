from configuration.config import EYE_DETECTION_CASCADE_PATH, DETECTION_RECORDS_PATH
from IO_operations.eyes_detection_record import append_detections_to_text_file
from flow_managment.task_flow_manager import TaskFlowManager
from generic.thread_helper import create_new_thread
import numpy as np
import time
import cv2


class FirstTaskFlowManager(TaskFlowManager):

    def __init__(self):
        self.eye_cascade = cv2.CascadeClassifier(EYE_DETECTION_CASCADE_PATH)
        self.default_camera_port = 1  # todo: change to 0
        self.capture = cv2.VideoCapture(self.default_camera_port)
        self.transparency = 0.2

    def _get_eye_box_list(self, frame, scaleFactor=1.3, minNeighbors=5):
        # The following method returns the coordinates for every eye detected
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.eye_cascade.detectMultiScale(gray, scaleFactor, minNeighbors)

    def _brighten_eye_box(self, frame):
        # TODO
        return frame

    # @staticmethod
    # def test(a):
    #     while True:
    #         print(f'a: {str(a)}')
    #         a += 1
    #         time.sleep(1)

    def _record_frame(self, frame):
        append_detections_to_text_file(r'C:\Users\ofir\Downloads\ttt.txt', frame)

    def _analyze_live_feed(self):
        """
        The following method gets 'live' frames from the configured camera port.
        The eyes in each frame will be brighten and every detection will be recorded using append_detections_to_text_file function

        * press 'q' to continue.
        """
        while True:
            _, frame = self.capture.read()
            overlay = frame.copy()
            eyes = self._get_eye_box_list(frame)
            if isinstance(eyes, np.ndarray) and len(eyes) == 0:
                p=0 # TODO
            for (x, y, w, h) in eyes:
                cv2.rectangle(overlay, (x, y), (x+w, y+h), (255, 255, 255), -1)
            frame = cv2.addWeighted(overlay, self.transparency, frame, 1 - self.transparency, 0)
            cv2.imshow('LiveVideo', frame)

            # record the frame in cases of detection
            # create_new_thread(self.test, a=2)

            if cv2.waitKey(1) & 0xFF == ord('q'):
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