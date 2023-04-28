import time
from typing import List
import numpy as np


def append_detections_to_text_file(filepath: str,
                                   single_frame_dets: List[np.ndarray]):
    with open(filepath, 'a') as f:
        f.write(f"{time.time()}\t")
        f.write(f"{[list(d) for d in single_frame_dets]}\n")
    time.sleep(0.1)  # e.g. send to a remote server
