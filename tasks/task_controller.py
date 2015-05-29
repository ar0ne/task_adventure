from task_service import TaskService
from datetime import datetime, timedelta
import pickle


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
        try:
            dbfile = open('data', "rb")
        except:
            print("[ERROR] File 'data' not found")
            return None
        controller = pickle.load(dbfile)
        dbfile.close()
        return controller

    def save(self):
        try:
            dbfile = open('data', "wb")
        except:
            print("[ERROR] File 'data' not found")
            return None
        pickle.dump(self, dbfile)
        dbfile.close()

    def time_left(self):
        """Calculate how much time left"""
        start = self._services._running_task.time_start
        end = self._services.running_task.time_end
        return end - start - (datetime.now() - start)

    def show_running_task(self):
        print("Title: " + self._services.running_task.title)
        print("Description: " + self._services.running_task.description)
        print("Time left: " + str(self.time_left()))

    def run(self):
        while(True):
            if self.status is False:
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
                    self.save()
                else:
                    print("Input not recognated. Try again")
            else:
                if self.check_running_task() is False:
                    continue
                str = raw_input("Type 'SHOW' - for show Task info\nType 'EXIT' for quit\nType 'ADD' for add new Task\n")
                if str.upper() == "SHOW":
                    self.show_running_task()
                elif str.upper() == "EXIT":
                    break
                elif str.upper() == "ADD":
                    title = raw_input("Enter Title of new task: ")
                    description = raw_input("Enter Description of new task: ")
                    self._services.add_task(title, description)
                    self.save()
                else:
                    print("Input not recognated. Try again")

    def check_running_task(self):
        if self.time_left() <= timedelta(seconds=0):
            self.status = False
            str = raw_input("Do you complete task?(Y/N)")
            if str.upper() == "Y":
                self._services._running_task = None
            elif str.upper() == "N":
                """Maybe add this task to opened tasks?"""
                # task = self._services._running_task
                # task.status = False  # That task can be
                # self._services.update_task(task)
                self._services._running_task = None
            return False
        else:
            return True
