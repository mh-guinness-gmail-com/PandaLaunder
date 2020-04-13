from threading import Thread
from queue import Queue
from typing import Callable, List


_stop_task = object()


class ThreadPool:
    def __init__(self, action: Callable, *, action_parameters: List, thread_count: int = 2):
        """Handle queue-based parallel work."""
        self.action = action
        self.action_parameters = action_parameters
        self.__queue = Queue()
        self.__threads = [
            Thread(target=self.__worker, args=[], daemon=True)for _ in range(thread_count)]

    def __start_threads(self):
        for t in self.__threads:
            t.start()

    def __stop_threads(self):
        # Wait for queue to empty
        self.__queue.join()
        # Send stop task to threads
        for _ in self.__threads:
            self.__queue.put(_stop_task)
        # Wait for all threads to end
        for thread in self.__threads:
            thread.join()

    def __enter__(self):
        """Starts the threads."""
        self.__start_threads()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Stops the threads."""
        self.__stop_threads()

    def __worker(self):
        for task in iter(self.__queue.get, _stop_task):
            try:
                tasks = self.action(task, *self.action_parameters)
                self.add_tasks(tasks)
            finally:
                self.__queue.task_done()

    def add_task(self, task):
        if task is _stop_task:
            raise ValueError(
                'Tried to enqueue a task that is used as a stop signal')
        self.__queue.put(task)

    def add_tasks(self, tasks):
        for task in tasks:
            self.add_task(task)
