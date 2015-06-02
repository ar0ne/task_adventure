from task_service import TaskService
from datetime import datetime, timedelta
import pickle


class TaskController:
    def __init__(self):
        self.status = False
        self.services = TaskService()

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
        start = self.services.running_task.time_start
        end = self.services.running_task.time_end
        return end - start - (datetime.now() - start)

    def is_running_task(self):
        """
        Check task status
        :return: False if not time left, True else
        """
        if self.services.running_task is None:
            return False
        if self.time_left() <= timedelta(seconds=0):
            return False
        else:
            return True
