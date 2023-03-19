from prelim_classes import MaxHeapq


class TaskScheduler:
    """
    Defining the TaskScheduler class

    Attributes
    ----------
    tasks : list[Task]
        a list of Task instances to put in the scheduler
    flexible_time_priority_queue : MinHeapq[Tasks]
        a maximum heap containing Task instances with no fixed execution times organized by priority
    fixed_time_priority_queue : MinHeapq[Tasks]
        a maximum heap containing Task instances with fixed execution times organized by starting time

    Methods
    -------
    print_self()
        Nicely prints out task descriptions and durations in the task sceduler and their respective dependencies if any
    get_tasks_ready()
        Populates flexible_time_priority_queue and fixed_time_prioruty queues with flexible-time tasks and fixed_time tasks respectively
    format_time(time)
        Returns a string representation of the time in the day from the time (in minutes) given
    run_task_scheduler(starting_time)
        Runs the tasks in the task scheduler in order of priorities (for flexible-time tasks) and starting times (for fixed-time tasks)
    """
    NOT_STARTED = "N"
    IN_PRIOIRITY_QUEUE = "I"
    IN_PROGRESS = "P"
    COMPLETED = "C"

    def __init__(self, tasks):
        self.tasks = tasks
        self.time_period = 7*60
        self.flexible_time_priority_queue = MaxHeapq()
        self.fixed_time_priority_queue = MaxHeapq()

    def print_self(self):
        """
        Nicely prints out task descriptions and durations in the task sceduler and their respective dependencies if any

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        print("Get these done today!")
        print("-----------------------")
        for task in self.tasks:
            print(
                f"-> '{task.description}', duration = {task.duration} minutes.")
            if task.dependencies:
                print(f"\tThis task depends on:")
                for dependency in task.dependencies:
                    print(
                        f"\t\t->⛔️'{dependency.description}', duration = {dependency.duration} minutes.")
                print()

    def get_tasks_ready(self):
        """
        Populates flexible_time_priority_queue and fixed_time_prioruty queues with flexible-time tasks and fixed_time tasks respectively

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        for task in self.tasks:
            if task.status != 'I':
                if not task.time:
                    self.flexible_time_priority_queue.heappush(task)
                else:
                    self.fixed_time_priority_queue.heappush(task)

            task.status = self.IN_PRIOIRITY_QUEUE

        # TEST CASES:
        # Check that all tasks have been added
        assert (len(self.fixed_time_priority_queue) +
                len(self.flexible_time_priority_queue) == len(self.tasks))
        # Check that all tasks in fixed_time_priority_queue have fixed times
        if self.fixed_time_priority_queue:
            assert ([fixed_task.time for fixed_task in self.fixed_time_priority_queue.heap] != [
                    None]*len(self.fixed_time_priority_queue))
        # Check that all tasks in flexible_time_priority_queue do not have fixed times
        assert ([flexible_task.time for flexible_task in self.flexible_time_priority_queue.heap] == [
                None]*len(self.flexible_time_priority_queue))

    def format_time(self, time):
        """
        Formats given time (in minutes) to a string showing hours and minutes (time in the day)

        Parameters
        ----------
        time : int/float
          time (in minutes) to be formatted

        Returns
        ----------
        str
          a string representation of the time in the day

        """
        return f"{int(time//60)}h{round(int(time%60), 2):02d}"

    def greedy_run_task_scheduler(self, starting_time, will_print=True):
        """
        Runs the tasks in the task scheduler in order of priorities (for flexible-time tasks) and starting times (for fixed-time tasks)
        using the greedy approach

        Parameters
        ----------
        starting_time : int/float
          time (in minutes) to start task scheduler
        will_print : bool
            whether to include print statements or not (included to avoid print statements in experimental time-complexity analysis)

        Returns
        ----------
        lst, int
            a lists of the order the tasks should be executed
            and the total utility for our task scheduler if will_print is False

        """
        # storing the order of execution of tasks
        tasks_order = []
        tasks_complete = []

        def print_done_task_helper(task, start_time):
            """
            Helper function that prints out a completed task and returns the time the task was completed

            Parameters
            ----------
            task : Task
                next completed task
            start_time : int/float
                start time for the task

            Returns
            ----------
            int
                end time (in minutes) of the task

            """
            task.status = self.IN_PROGRESS
            end_time = start_time + task.duration
            if end_time > starting_time + self.time_period:
                return start_time
            will_print and print(f"⌚️t={self.format_time(start_time)}")
            will_print and print(
                f"\tstarted '{task.description}' for {task.duration} mins...")
            # add task to tasks_order
            tasks_order.append(task)
            tasks_complete.append(task)
            # end_time = start_time + task.duration
            will_print and print(
                f"\t✅t={self.format_time(end_time)}, task completed with utility {round(1/task.unimportance(), 2)}!\n")
            task.status = self.COMPLETED

            return end_time

        def check_free_time_helper(current_time, fixed_time_task):
            """
            Helper function that checks if there's free time available given the current time and a fixed-time task

            Parameters
            ----------
            current_time : int/float
                curent time (in mintutes)
            fixed_time_task : Task
                next fixed-time task to be completed

            Returns
            ----------
            int
                current_time (in minutes) after the free time period

            """
            fixed_start_time = fixed_time_task.time*60

            if current_time != fixed_start_time:
                resting_time = fixed_start_time - current_time

                if current_time + resting_time > starting_time + self.time_period:
                    return current_time

                will_print and print(f"⌚️t={self.format_time(current_time)}")
                will_print and print(
                    f"\tFREE TIME for {resting_time} mins... 🤪")

                current_time += resting_time

            return current_time

        current_time = starting_time
        will_print and print("Running Somto's Greedy scheduler:\n")
        self.get_tasks_ready()

        # while there are tasks in the flexible and fixed time tasks priority queues
        while self.flexible_time_priority_queue and self.fixed_time_priority_queue:

            # query both the flexible and fixed time tasks priority queues
            flexible_time_task = self.flexible_time_priority_queue.maxk()
            timed_task = self.fixed_time_priority_queue.maxk()

            # if completing the flexible time task eats into the timed task start time
            if current_time+flexible_time_task.duration > timed_task.time*60:
                # next task to be completed will be the fixed time task
                next_task = self.fixed_time_priority_queue.heappop()
                # check for free time and update current time
                current_time = check_free_time_helper(current_time, next_task)
            # otherwise
            else:
                # next task to be completed will be the flexible time task
                next_task = self.flexible_time_priority_queue.heappop()
            # print completed task and update current time
            current_time = print_done_task_helper(next_task, current_time)

        # while there are still tasks in the fixed time priority queue
        while self.fixed_time_priority_queue:
            # complete the remaining fixed time tasks
            next_task = self.fixed_time_priority_queue.heappop()
            end_free_time = check_free_time_helper(current_time, next_task)
            current_time = print_done_task_helper(next_task, end_free_time)

        # while there are still tasks in the flexible time priority queue
        while self.flexible_time_priority_queue:
            # complete the remaining flexible time tasks
            next_task = self.flexible_time_priority_queue.heappop()
            current_time = print_done_task_helper(next_task, current_time)

        # total completion time
        total_time = current_time - starting_time
        will_print and print(
            f"\n🏁 Completed all planned tasks in {self.format_time(total_time)}min!")
        total_utility = sum([1/task.unimportance() for task in tasks_order])
        will_print and print(f"Total utility: {round(total_utility, 2)}")

        return (tasks_order, total_utility) if not will_print else None

    def dp_run_task_scheduler(self, starting_time, will_print=True):
        """
        Runs the tasks in the task scheduler in order of priorities (for flexible-time tasks) and starting times (for fixed-time tasks)
        using the dynamic programming approach

        Parameters
        ----------
        starting_time : int/float
          time (in minutes) to start task scheduler
        will_print : bool
            whether to include print statements or not (included to avoid print statements in experimental time-complexity analysis)

        Returns
        ----------
        lst, int
            a lists of the order the tasks should be executed
            and the total utility for our task scheduler if will_print is False

        """
        total_utility = 0
        tasks_order = []

        will_print and print(
            "Running Somto's Dynamic Programming scheduler:\n")
        self.get_tasks_ready()

        def get_optimal_tasks_helper(capacity):
            """
            Helper function that generates the dynamic programming matrix given a time constraint

            Parameters
            ----------
            capacity : int/float
                time constraint for the tasks

            Returns
            ----------
            list[list]
                dynamic programming matrix that gives maximum utility

            """
            # nothing can be done
            if capacity <= 0 or n == 0:
                return 0

            # dynamic programming matrix
            dp_matrix = [[0 for _ in range(capacity+1)] for _ in range(n)]

            # populate the time slot = 0 columns, with no time we have no utility
            for row in range(0, n):
                dp_matrix[row][0] = 0

            # if we have only one time slot, we will take a task if its duration is within the time slot and store utility = 1/unimportance level
            for c in range(0, capacity+1):
                if tasks[0].duration <= c*30:
                    dp_matrix[0][c] = round(1/tasks[0].unimportance(), 2)

            # process all sub-arrays for all the time slots
            for row in range(1, n):
                for c in range(1, capacity+1):
                    util1, util2 = 0, 0
                    # include the item, if it fits within the time slot
                    if tasks[row].duration <= c*30 and int(c - tasks[row].duration/30) >= 0:
                        util1 = round(round(
                            1/tasks[row].unimportance(), 2) + dp_matrix[row - 1][c - tasks[row].duration//30], 2)
                    # exclude the item
                    util2 = dp_matrix[row - 1][c]
                    # take maximum
                    dp_matrix[row][c] = max(util1, util2)

            # maximum profit will be at the bottom-right corner.
            res = dp_matrix[n - 1][capacity]
            return dp_matrix

        def read_dp_table_helper(table, capacity):
            """
            Helper function that generates the optimal tasks given a dynamic programming matrix

            Parameters
            ----------
            table : list
                time constraint for the tasks
            capacity : int/float
                time constraint for the tasks

            Returns
            ----------
            list
                the optimal tasks from the dynamic programming matrix

            """
            # store optimal tasks
            optimal_tasks = []
            # reading baclwards from bottom right
            for row in range(n-1, -1, -1):
                # if current cell is same as above
                if table[row][capacity] == table[row-1][capacity] and row != 0:
                    # and current cell is at row 1
                    if row == 1:
                        # row 0 is the optimal task
                        optimal_tasks.append(tasks[0])
                        break
                    # otherwise, move on to next row
                    else:
                        continue
                # if current cell not same as above
                else:
                    # the current row represents an optimal task
                    optimal_tasks.append(tasks[row])
                    # reduce capacity by the optimal task's duration
                    capacity -= tasks[row].duration // 30

            return optimal_tasks

        def print_optimal_tasks_helper(capacity, utility, current_time):
            """
            Helper function that prints the optimal tasks and returns the time after completion as well as the utility

            Parameters
            ----------
            capacity : int/float
                time constraint for the tasks
            utility : int/float
                total task scheduler utility so far
            current_time : int/float
                current scheduler time

            Returns
            ----------
            tuple(int, int)
                the total utility and the current time after completing these tasks

            """
            # get the optimal tasks
            table = get_optimal_tasks_helper(capacity)
            if table == 0:
                optimal_tasks = []
            else:
                optimal_tasks = read_dp_table_helper(table, capacity)

            # heap to organize our tasks by priority
            optimal_heap = MaxHeapq()
            for task in optimal_tasks:
                optimal_heap.heappush(task)

            # complete tasks by priority
            while optimal_heap:
                task = optimal_heap.heappop()
                # remove task from tasks list after completion
                tasks.remove(task)
                # increase task scheduler utility by the task's util
                utility += 1/task.unimportance()

                task.status = self.IN_PROGRESS
                will_print and print(f"⌚️t={self.format_time(current_time)}")
                will_print and print(
                    f"\tstarted '{task.description}' for {task.duration} mins...")
                # add task to tasks_order
                tasks_order.append(task)
                current_time += task.duration
                will_print and print(
                    f"\t✅t={self.format_time(current_time)}, task completed with utility {round(1/task.unimportance(), 2)}!\n")
                task.status = self.COMPLETED

            return utility, current_time

        # get the tasks ready
        for task in self.tasks:
            if task.status != 'I':
                task.status = self.NOT_STARTED
        if len(self.fixed_time_priority_queue)+len(self.flexible_time_priority_queue) < len(self.tasks):
            self.get_tasks_ready()

        # we use only flexible time tasks for the dp tables
        tasks = self.flexible_time_priority_queue.heap[:]

        current_time = starting_time
        max_time = starting_time + self.time_period

        # if there are no fixed time tasks
        if not self.fixed_time_priority_queue:
            n = len(tasks)
            # capacity is our task scheduler's total capacity
            capacity = int((max_time - current_time) // 30)
            # show tasks and update current time and utility
            util, current_time = print_optimal_tasks_helper(
                capacity, total_utility, current_time)
            total_utility = util

        # if there are fixed time tasks
        while self.fixed_time_priority_queue and current_time < max_time:
            n = len(tasks)
            tasks = sorted(tasks, key=lambda x: x.duration)

            # get the time for the next task
            next_timed_task = self.fixed_time_priority_queue.heappop()
            next_time = next_timed_task.time*60
            next_timed_task.status = self.IN_PROGRESS
            # if the time is within our constraint
            if next_time < max_time:
                # the capacity is the time chunk between current time and next fixed time
                capacity = int((next_time - current_time) // 30)
            # otherwise
            else:
                # the capacity is the remaining time left within our constraint
                capacity = int((max_time - current_time) // 30)
            # show tasks and update current time and utility
            util, current_time = print_optimal_tasks_helper(
                capacity, total_utility, current_time)
            total_utility = util

            # show fixed time task if it can be completed within our constraint
            if next_time < max_time:
                next_timed_task.status = self.IN_PROGRESS
                total_utility += 1/next_timed_task.unimportance()

                will_print and print(f"⌚️t={self.format_time(current_time)}")
                will_print and print(
                    f"\tstarted '{next_timed_task.description}' for {next_timed_task.duration} mins...")

                current_time += next_timed_task.duration
                will_print and print(
                    f"\t✅t={self.format_time(current_time)}, task completed with utility {round(1/task.unimportance(), 2)}!\n")
                next_timed_task.status = self.COMPLETED

        # show the total time for completion as well as utility
        total_time = current_time - starting_time
        will_print and print(
            f"\n🏁 Completed all planned tasks in {self.format_time(total_time)}min!")
        will_print and print(f"Total utility: {round(total_utility,2)}")

        return (tasks_order, total_utility) if not will_print else None
