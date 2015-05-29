


class Task:
    def __init__(self, id, title, description, time_start, time_end, status=False):
        self._id = id
        self._title = title
        self._description = description
        self._time_start = time_start
        self._time_end = time_end
        self._status = status

    def is_done(self):
        return self._status

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def time_start(self):
        return self._time_start

    @time_start.setter
    def time_start(self, value):
        self._time_start = value

    @property
    def time_end(self):
        return self._time_end

    @time_end.setter
    def time_end(self, value):
        self._time_end = value

    def __str__(self):
        return ("ID: " + self._id +
                "\nTITLE: " + self._title +
                "\nDESCRIPTION: " + self._description +
                "\nSTATUS: " + self._status +
                "\nTIME START: " + self.time_start +
                "\nTIME END: " + self.time_end)

