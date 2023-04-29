from flow_managment.main_flow_manager import MainFlowManager
from configuration import config

# todo
"""
mention the need for a production ready and scalable project in the readme. must support additional tasks.
"""

task_list = [1, 2]


def main():

    for task in task_list:
        MainFlowManager().handle_task(task_id=task)

    pass
