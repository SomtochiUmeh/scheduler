from taskscheduler import TaskScheduler
from prepare_tasks import to_do_tasks

my_schedule = TaskScheduler(to_do_tasks)
start = 4*60
my_schedule.greedy_run_task_scheduler(start)
