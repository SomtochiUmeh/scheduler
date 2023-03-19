class Task:

    """
    Defining the Task class

    Attributes
    ----------
    id : int
        a unique identifier (that other tasks can reference)
    description : str
        short description of task
    duration : int
        how long the task takes in minutes
    dependencies : list
        list of tasks ids which must be completed before this task instance
    status : str
        state of task: not started, in priority queue, or completed (default "N")
    time : int
        fixed time a task is to run if a fixed time exists (default None)

    Methods
    -------
    priority()
        returns the calculated priority value of a task instance
    __lt__(other: Task)
        determines if the task instance is less than the passed in task instance
    """

    def __init__(self, id, description, duration, dependencies=[], status="N", time=None):
        self.id = id
        self.description = description
        self.duration = duration
        self.dependencies = dependencies
        self.status = status
        self.time = time

    def unimportance(self):
        """
        Calculates the priority value of a task instance

        Parameters
        ----------
        None

        Returns
        ----------
        int
          Priority value of task instance

        """
        # dummy Task instance for handling heappush to Minheap
        if self.description == 'dummy':
            return float('inf')
        # priority value calculation using number of dependencies, duration, and individual priorities of each of the dependencies
        unimportance_score = len(self.dependencies) + self.duration/60
        for task in self.dependencies:
            unimportance_score += task.unimportance()

        return unimportance_score

    def __lt__(self, other):
        """
        Determines if the left operand is less than the right operand

        Parameters
        ----------
        other : Task
          instance of task class to compare current instance with

        Returns
        ----------
        bool
          whether or not the left operand is less than the right operand

        """
        # for fixed-time tasks, tasks starting earlier would be at the top of the priority queue
        if self.time and other.time:
            return self.time > other.time
        # for flexible time tasks, tasks with smaller priority values would be at the top of the priority queue
        return 1/self.unimportance() < 1/other.unimportance()


class MaxHeapq:
    """
    Defining the MaxHeapq class

    Attributes
    ----------
    heap : list
        the array representation of the max heap
    heap_size : int
        number of values in the heap

    Methods
    -------
    left(i)
        Takes the index of the parent node and returns the index of the left child node
    right(i)
        Takes the index of the parent node and returns the index of the right child node
    parent(i)
        Takes the index of the child node and returns the index of the parent node
    maxk()
        Returns the highest key in the priority queue
    heappush(key: Task)
        Insert a key (Task instance) into a priority queue 
    increase_key(i, key)
        Modifies the value of a key in a max priority queue with a higher value
    heapify(i)
        Creates a max heap from the index given
    heappop()
        Returns the largest key in the max priority queue and removes it from the max priority queue
    __len__()
        Returns the heap's length
    """

    def __init__(self):
        self.heap = []
        self.heap_size = 0

    def left(self, i):
        """
        Takes the index of the parent node
        and returns the index of the left child node

        Parameters
        ----------
        i: int
          Index of parent node

        Returns
        ----------
        int
          Index of the left child node

        """
        return 2 * i + 1

    def right(self, i):
        """
        Takes the index of the parent node
        and returns the index of the right child node

        Parameters
        ----------
        i: int
            Index of parent node

        Returns
        ----------
        int
            Index of the right child node

        """

        return 2 * i + 2

    def parent(self, i):
        """
        Takes the index of the child node
        and returns the index of the parent node

        Parameters
        ----------
        i: int
            Index of child node

        Returns
        ----------
        int
            Index of the parent node

        """

        return (i - 1)//2

    def maxk(self):
        """
        Returns the highest key in the priority queue. 

        Parameters
        ----------
        None

        Returns
        ----------
        int
            the highest key in the priority queue

        """
        return self.heap[0]

    def heappush(self, key):
        """
        Insert a key into a priority queue 

        Parameters
        ----------
        key: int
            The key value to be inserted

        Returns
        ----------
        None
        """
        self.heap.append(Task(-float('inf'), 'dummy', 0, []))
        self.increase_key(self.heap_size, key)
        self.heap_size += 1

    def increase_key(self, i, key):
        """
        Modifies the value of a key in a max priority queue
        with a higher value

        Parameters
        ----------
        i: int
            The index of the key to be modified
        key: int
            The new key value

        Returns
        ----------
        None
        """
        if key < self.heap[i]:
            raise ValueError('new key is smaller than the current key')
        self.heap[i] = key
        while i > 0 and self.heap[self.parent(i)] < self.heap[i]:
            j = self.parent(i)
            holder = self.heap[j]
            self.heap[j] = self.heap[i]
            self.heap[i] = holder
            i = j

    def heapify(self, i):
        """
        Creates a max heap from the index given

        Parameters
        ----------
        i: int
            The index of of the root node of the subtree to be heapify

        Returns
        ----------
        None
        """
        l = self.left(i)
        r = self.right(i)
        heap = self.heap
        if l <= (self.heap_size-1) and heap[l] > heap[i]:
            largest = l
        else:
            largest = i
        if r <= (self.heap_size-1) and heap[r] > heap[largest]:
            largest = r
        if largest != i:
            heap[i], heap[largest] = heap[largest], heap[i]
            self.heapify(largest)

    def heappop(self):
        """
        Returns the largest key in the max priority queue
        and remove it from the max priority queue

        Parameters
        ----------
        None

        Returns
        ----------
        int
            the max value in the heap that is extracted
        """
        if self.heap_size < 1:
            raise ValueError(
                'Heap underflow: There are no keys in the priority queue ')
        maxk = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self.heap_size -= 1
        self.heapify(0)
        return maxk

    def __len__(self):
        """
        Returns the heap's length

        Parameters
        ----------
        None

        Returns
        ----------
        int
            the heap size
        """
        return self.heap_size
