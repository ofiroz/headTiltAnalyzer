from flow_managment.main_flow_manager import MainFlowManager
from configuration import config


# Production ready and scalable project todo readme.
# The project supports additional tasks.


task_list = [1, 2]


def main():
    for task in task_list:
        # todo: log
        MainFlowManager().handle_task(task_id=task)
        # todo: log
    # todo: log


if __name__ == '__main__':
    main()

