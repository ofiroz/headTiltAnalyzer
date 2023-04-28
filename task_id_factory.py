from flow_managment.flow_managers.first_task_flow_manager import FirstTaskFlowManager
from flow_managment.flow_managers.second_task_flow_manager import SecondTaskFlowManager


class TaskIdFactory:
    task_id_mapping = {'1': 'FirstTask',
                       '2': 'SecondTask'}

    @classmethod
    def get_instance(cls, task_id: str, instance: str, static=False):
        try:
            task_id = cls.task_id_mapping.get(task_id[0], None)
            eval_string = '()' if not static else ''
            return eval(f'{task_id}{instance}{eval_string}')
        except Exception as e:
            msg = f'unable to initiate instance: {task_id}, {instance}'
            raise NotImplementedError(msg)
