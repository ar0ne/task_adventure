from task import Task
from datetime import datetime, timedelta
from random import randint


class TaskService:
    def __init__(self, tasks=[]):
        self.tasks = tasks
        self.running_task = None

    def get_closed_tasks(self, count=0):
        """Get all(or count) tasks with status Done == True"""
        tasks_closed = []
        if count == 0:  # get all closed tasks
            for t in self.tasks:
                if t.status is True:
                    tasks_closed.append(t)
            return tasks_closed
        else:  # get how much we can or count
            for t in self.tasks:
                if count <= 0:
                    break
                if t.status is True:
                    tasks_closed.append(t)
                    count -= 1
            return tasks_closed

    def get_opened_tasks(self, count=0):
        """Get all(or count) tasks with status Done == False"""
        tasks_open = []
        if count == 0:  # get all closed tasks
            for t in self.tasks:
                if t.status is True:
                    tasks_open.append(t)
            return tasks_open
        else:  # get how much we can or count
            for t in self.tasks:
                if count <= 0:
                    break
                if t.status is True:
                    tasks_open.append(t)
                    count -= 1
            return tasks_open

    def get_last_id(self):
        """Get last id in tasks"""
        last_id = 0
        for task in self.tasks:
            if not task.id is None and task.id > last_id:
                last_id = task.id
        return last_id

    def get_last_k_closed_tasks(self, k=0):
        """Get last k or less closed tasks if it's impossible"""
        if k is not 0:
            all_closed_tasks = self.get_closed_tasks()
            foo = []
            for task in all_closed_tasks:
                foo.append((task.time_end, task))
            last_k = sorted(foo)[-k:]  # sort by index and get k-last tasks
            out = []
            for task in reversed(last_k):  # reverse before return
                out.append(task[1])
            return out
        return None

    def add_task(self, task):
        if task is None:
            raise Exception("[WARNING] Task can't be NULL")
        self.tasks.append(task)

    def add_task(self, description):
        if description is None:
            raise Exception("[WARNING] Description of new task can't be empty")
        task = Task(self.get_last_id() + 1, description, None, None, status=False)
        self.tasks.append(task)

    def update_task(self, task):
        index = self.find_task_by_id(task.id)
        if index is None:
            raise Exception("[ERROR] Task not found")
        else:
            self.tasks[index] = task

    def delete_task(self, task):
        index = self.find_task_by_id(task.id)
        if index is None:
            raise Exception("[WARNING] Task not found")
        else:
            self.tasks.pop(index)

    def find_task_by_id(self, task_id):
        t = [t for t in self.tasks if t.id == task_id]  # find old task in task by Id
        if len(t) == 0:
            return None
        elif len(t) > 1:
            raise Exception("[ERROR] Tasks with the same Id in Database, id = " + task_id)
        if len(t) == 1:
            return self.tasks.index(t[0])

    def start_random_task(self):
        available_tasks = self.get_opened_tasks()
        task = None
        if len(available_tasks) == 0:
            print("[WARNING] Database don't have task for you. Try to add something")
            return False
        elif len(available_tasks) == 1:
            task = available_tasks[0]
        else:
            available_tasks_index = [self.tasks.index(task) for task in available_tasks]
            rand_task_index = available_tasks_index[randint(0, len(available_tasks_index) - 1)]
            task = self.tasks[rand_task_index]
        now = datetime.now()
        task = Task(task.id, task.description, now, now + timedelta(seconds=24), True)
        self.update_task(task)
        self.running_task = task
        return True




