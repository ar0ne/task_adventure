from task import Task
from datetime import datetime, timedelta
from random import randint


class TaskService:
    def __init__(self, tasks=[]):
        self._tasks = tasks
        self._running_task = None

    def get_closed_tasks(self):
        """Get all tasks with status Done == True"""
        tasks_done = []
        for t in self._tasks:
            if t.is_done():
                tasks_done.append(t)
        return tasks_done

    def get_opened_tasks(self):
        """Get all tasks with status Done == False"""
        tasks_open = []
        for t in self._tasks:
            if not t.is_done():
                tasks_open.append(t)
        return tasks_open

    def get_last_id(self):
        """Get last id in tasks"""
        last_id = 0
        for task in self._tasks:
            if not task._id is None and task._id > last_id:
                last_id = task._id
        return last_id

    def add_task(self, task):
        if task is None:
            print("[WARNING] Task can't be NULL")
        self._tasks.append(task)

    def add_task(self, title=None, description=None):
        if title is None or description is None:
            print("[WARNING] Title and Description of new task can't be empty")
            return
        task = Task(self.get_last_id() + 1, title, description, None, None, status=False)
        self._tasks.append(task)

    def update_task(self, task):
        index = self.find_task_by_id(task.id)
        if index is None:
            print("[ERROR] Task not found")
        else:
            self._tasks[index] = task

    def delete_task(self, task):
        index = self.find_task_by_id(task.id)
        if index is None:
            print("[WARNING] Task not found")
        else:
            self._tasks.pop(index)

    def find_task_by_id(self, task_id):
        t = [t for t in self._tasks if t.id == task_id]  # find old task in task by Id
        if len(t) == 0:
            return None
        elif len(t) > 1:
            raise Exception("[ERROR] Tasks with the same Id in Database, id = " + task_id)
        if len(t) == 1:
            return self._tasks.index(t[0])

    def start_random_task(self):
        available_tasks = self.get_opened_tasks()
        task = None
        if len(available_tasks) == 0:
            print("[WARNING] Database don't have task for you. Try to add something")
            return False
        elif len(available_tasks) == 1:
            task = available_tasks[0]
        else:
            available_tasks_index = [self._tasks.index(task) for task in available_tasks]
            rand_task_index = available_tasks_index[randint(0, len(available_tasks_index) - 1)]
            task = self._tasks[rand_task_index]
        now = datetime.now()
        task = Task(task.id, task.title, task.description, now, now + timedelta(seconds=24), True)
        self.update_task(task)
        self._running_task = task
        return True

    @property
    def running_task(self):
        return self._running_task

    @running_task.setter
    def running_task(self, task):
        self._running_task = task






