from tasks import somtos_tasks
from prelim_classes import Task


def prepare_tasks(tasks):
    """
    Creates a task object for each task in tasks

    Parameters
    ----------
    tasks : list[dict]
        a list of dictionaries with each dictionary containing necessary data for the Task class

    Returns
    ----------
    list
        a list of Task objects for each task in tasks

    """
    # stores the Task instances for the tasks passed into the function
    task_instances = []

    # for each passed in task
    for task in tasks:
        # get its id, description, duration and dependencies
        id = task['id']
        description = task['description']
        duration = task['duration']
        dependencies = task['dependencies']
        # get the time for the fixed time tasks; assign time to None if it's a time-flexible task
        time = task.get('time', None)

        # transform the task into a task instance
        task_instances.append(
            Task(id, description, duration, dependencies, time=time))

    def get_task_dependencies_helper(ids):
        """
        Maps task instances with their corresponding ids

        Parameters
        ----------
        ids : list
          list of ids to get task instances of

        Returns
        ----------
        list
          list of task instances corresponding to ids

        """
        # stores list of task instances from the given ids
        dependencies_instances = []

        # for each task object in list to_do tasks
        for task in task_instances:
            # if the task id is in the given list of task ids
            if task.id in ids:
                # then that task object is the corresponding task instance for the id
                dependencies_instances.append(task)

        return dependencies_instances

    # for each task instance in to_do_tasks
    for task in task_instances:
        # transform its dependencies list from ids to Task instances
        task.dependencies = get_task_dependencies_helper(task.dependencies)

    return task_instances


to_do_tasks = prepare_tasks(somtos_tasks)
