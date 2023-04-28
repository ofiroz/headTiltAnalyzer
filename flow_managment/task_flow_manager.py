from abc import abstractmethod

class TaskFlowManager:

    @staticmethod
    @abstractmethod
    def flow():
        """
        Runs the entire task step by step.
        Steps will be specified in each implementation.
        """
        pass

    @staticmethod
    @abstractmethod
    def clean_task():
        pass
