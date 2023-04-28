from flow_managment.task_flow_manager import TaskFlowManager
from task_id_factory import TaskIdFactory
from typing import Union


class MainFlowManager:

    def handle_task(self, task_id: Union[int, str]):
        # todo: init logger
        try:
            flow_manager: TaskFlowManager = TaskIdFactory.get_instance(str(task_id), 'FlowManager')

        except KeyError as e:
            print('task failed')
            # todo: logger.error
