from threading import Thread
from typing import Callable


def create_new_thread(func: Callable, *args, **kwargs):
    t = Thread(target=lambda: func(*args, **kwargs))
    t.start()
