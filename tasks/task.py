
class Task:
    def __init__(self, id, description, time_start, time_end, status=False):
        self.id = id
        self.description = description
        self.time_start = time_start
        self.time_end = time_end
        self.status = status

    def __str__(self):
        return ("ID: " + self.id +
                "\nDESCRIPTION: " + self.description +
                "\nSTATUS: " + self.status +
                "\nTIME START: " + self.time_start +
                "\nTIME END: " + self.time_end)

