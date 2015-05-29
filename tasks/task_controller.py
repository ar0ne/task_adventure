from task_service import TaskService
from datetime import datetime, timedelta


class TaskController:
    def __init__(self):
        self._status = False
        self._services = TaskService()

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @staticmethod
    def load():
        pass

    def save(self):
        pass

    def time_left(self, start, end):
        """Calculate how much time left"""
        return end - start - (datetime.now() - start)

    def show_running_task(self):
        print("Title: " + self._services.running_task.title)
        print("Description: " + self._services.running_task.description)
        print("Time left: " + str(self.time_left(self._services._running_task.time_start, self._services.running_task.time_end)))

    def run(self):
        while(True):
            if self.status == False:
                str = raw_input("You can start your adventure now, just type 'START'\nOr you can add new Task, type 'ADD'\n")
                if str.upper() == "START":
                    ret = self._services.start_random_task()
                    if ret is True:
                        self.status = True
                        self.save()
                    continue
                elif str.upper() == "ADD":
                    title = raw_input("Enter Title of new task: ")
                    description = raw_input("Enter Description of new task: ")
                    self._services.add_task(title, description)
                else:
                    print("Input not recognated. Try again")
            else:
                str = raw_input("Type 'SHOW' - for show Task info\nType 'EXIT' for quit\n")
                if str.upper() == "SHOW":
                    self.show_running_task()
                elif str.upper() == "EXIT":
                    break