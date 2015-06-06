from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.base import EventLoop
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView
from kivy.adapters.models import SelectableDataItem

from tasks import TaskController

__version__ = "1.0"


class TaskAdventure(Widget):
    pass


class AddTaskDialog(Screen):

    description = ObjectProperty(None)

    def save(self):

        description = self.description.text.strip().replace("\t", " ")

        if len(description) == 0:
            EmptyTaskPopup().open()

            return False

        elif len(description) > 300:
            TooLongTaskDescriptionPopup().open()
            return False

        controller.services.add_task(description)
        controller.save()

        self.description.text = ""

        sm.transition.direction = 'left'

        if controller.status is False:
            sm.current = "wait_task"
        else:
            sm.current = "run_task"

    def cancel(self):

        self.description.text = ""

        sm.transition.direction = 'left'

        if controller.status is False:
            sm.current = "wait_task"
        else:
            sm.current = "run_task"


class WaitTaskDialog(Screen):

    closed_tasks_panel = ObjectProperty(None)

    def on_pre_enter(self, *args):
        closed_tasks = controller.services.get_last_k_closed_tasks(4)  # get last 4 closed tasks
        for index, task in enumerate(closed_tasks):
            self.closed_tasks_panel.add_widget( ClosedTaskPreview(task.description, task.time_end) )

    def on_leave(self, *args):
        self.closed_tasks_panel.clear_widgets()

    def start(self):

        ret = controller.services.start_random_task()

        if ret is True:
            controller.status = True
            controller.save()

            sm.transition.direction = 'up'
            sm.current = "run_task"
        else:
            EmptyDatabasePopup().open()


class RunningTaskDialog(Screen):

    description = ObjectProperty(None)
    clock = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.update()
        self.description.text = str(controller.services.running_task.description)
        Clock.schedule_interval(self.update, 1)

    def on_pre_leave(self, *args):
        Clock.unschedule(self.update)

    def update(self, dt=None):
        if controller.is_running_task() is False:

            CompleteTaskPopup().open()

            controller.status = controller.is_running_task()
            controller.services.running_task = None

            controller.save()

            sm.transition.direction = 'down'
            sm.current = "wait_task"
        else:
            self.clock.text = str(controller.time_left()).split(".")[0]  # remove milliseconds

    def clock_button_callback(self):
        CompleteTaskEarlyPopup().open()


class ClosedTaskPreview(BoxLayout):

    short_description = ObjectProperty(None)
    date = ObjectProperty(None)

    def __init__(self, description=None, date=None, **kwargs):
        super(ClosedTaskPreview, self).__init__(**kwargs)

        if not description is None:
            self.short_description.text = str(description)[:20] + "..."
        if not date is None:
            self.date.text = date.strftime("%d.%m.%Y")

    def show_closed_task_dialog(self, button):
        # print("Show " + button.parent.short_description.text )
        sm.transition.direction = 'left'
        sm.current = "closed_tasks"


class ClosedTaskDialog(Screen):

    closed_task_listview = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.closed_task_listview.add_widget(ClosedTaskListView())

    def on_leave(self, *args):
        self.closed_task_listview.clear_widgets()


class DataItem(SelectableDataItem):
    """Class wrapper for task instance, need it for ListView"""
    def __init__(self, description='', time_start="", time_end="", **kwargs):
        super(DataItem, self).__init__(**kwargs)
        self.description = description
        self.time_start = "Started:  " + str(time_start).split(".")[0]  # cut milliseconds
        self.time_end = "Ended:    " + str(time_end).split(".")[0]

class CustomListItem(BoxLayout):

    description = ObjectProperty(None)
    time_start =  ObjectProperty(None)
    time_end =    ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CustomListItem, self).__init__(**kwargs)
        self.description.text = kwargs['description']
        self.time_start.text =  kwargs['time_start']
        self.time_end.text =    kwargs['time_end']

class ClosedTaskListView(BoxLayout):
    def __init__(self, **kwargs):
        super(ClosedTaskListView, self).__init__(**kwargs)
        closed_tasks = controller.services.get_closed_tasks()

        data_items = [DataItem(description=task.description,
                               time_end=task.time_end,
                               time_start=task.time_start) for task in closed_tasks]

        list_item_args_converter = lambda row_index, obj: {'description': obj.description,
                                                           'time_start': obj.time_start,
                                                           'time_end': obj.time_end,
                                                           'size_hint_y': None}

        list_adapter = ListAdapter( data=data_items,
                                    args_converter=list_item_args_converter,
                                    propagate_selection_to_data=True,
                                    cls='CustomListItem')

        master_list_view = ListView(adapter=list_adapter,
                                    size_hint=(.3, 1.0))

        self.add_widget(master_list_view)



class TaskAdventureApp(App):

    def __init__(self, **kwargs):
        super(TaskAdventureApp, self).__init__(**kwargs)
        Window.bind(on_keyboard=self.on_back_btn)

    def build(self):

        EventLoop.window.clearcolor = (0.247, 0.318, 0.71, 1)  # set blue color as base background color instead black

        sm.add_widget(WaitTaskDialog(name='wait_task'))
        sm.add_widget(AddTaskDialog(name='add_task'))
        sm.add_widget(RunningTaskDialog(name='run_task'))
        sm.add_widget(ClosedTaskDialog(name='closed_tasks'))

        sm.transition.direction = 'up'

        controller.status = controller.is_running_task()

        if controller.status is False:
            if controller.services.running_task is None:
                sm.current = 'wait_task'
            else:
                CompleteTaskPopup().open()

                controller.services.running_task = None

                controller.save()

                sm.current = 'wait_task'

        else:
            sm.current = 'run_task'

        return sm

    def on_back_btn(self, window, key, *args):
        """ To be called whenever user presses Back/Esc Key """
        # If user presses Back/Esc Key
        if key == 27:
            ExitPopup().open()
            return True
        return False

class OneButtonPopup(Popup):
    """Base class for one button popup modal windows"""
    def on_press_dismiss(self, *args):
        self.dismiss()
        return False

class EmptyDatabasePopup(OneButtonPopup):

    close_button = ObjectProperty(None)
    content_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(EmptyDatabasePopup, self).__init__(**kwargs)
        self.close_button.text = "OK"
        self.content_label.text = "Please, add few tasks manually."
        self.title = 'Empty Database'


class EmptyTaskPopup(OneButtonPopup):

    close_button = ObjectProperty(None)
    content_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(EmptyTaskPopup, self).__init__(**kwargs)
        self.close_button.text = "OK"
        self.content_label.text = "Task can't be empty."
        self.title = 'Empty Task'


class TooLongTaskDescriptionPopup(OneButtonPopup):

    close_button = ObjectProperty(None)
    content_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TooLongTaskDescriptionPopup, self).__init__(**kwargs)
        self.close_button.text = "OK"
        self.content_label.text = "Task can't be more then 300 chars."
        self.title = 'Task too long'


class TwoButtonPopup(Popup):
    """Base class for popup with 2 buttons like: "Yes" and "No" with own callbacks"""
    def first_button_callback(self):
        pass

    def second_button_callback(self):
        pass


class CompleteTaskPopup(TwoButtonPopup):

    first_button = ObjectProperty(None)
    second_button = ObjectProperty(None)
    content_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CompleteTaskPopup, self).__init__(**kwargs)
        self.title = 'Time out'
        self.content_label.text = "Do you complete quest?"
        self.first_button.text = "Yes"
        self.second_button.text = "No"

    def first_button_callback(self):
        self.dismiss()
        return False

    def second_button_callback(self):
        self.dismiss()
        return False


class ExitPopup(TwoButtonPopup):

    first_button =  ObjectProperty(None)
    second_button = ObjectProperty(None)
    content_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(ExitPopup, self).__init__(**kwargs)
        self.title = 'Exit'
        self.content_label.text = "Do you want to exit?"
        self.first_button.text = "Yes"
        self.second_button.text = "No"

    def first_button_callback(self):
        """Kill application"""
        App.get_running_app().stop()
        return True

    def second_button_callback(self):
        """Close popup"""
        self.dismiss()
        return False


class CompleteTaskEarlyPopup(TwoButtonPopup):

    first_button = ObjectProperty(None)
    second_button = ObjectProperty(None)
    content_label = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CompleteTaskEarlyPopup, self).__init__(**kwargs)
        self.title = 'Complete task'
        self.content_label.text = "You have already completed the task?"
        self.first_button.text = "Yes"
        self.second_button.text = "No"

    def first_button_callback(self):
        """Stop running current task"""
        controller.status = False
        controller.services.running_task = None
        self.dismiss()
        return False

    def second_button_callback(self):
        """Close popup"""
        self.dismiss()
        return False


if __name__ == '__main__':

    sm = ScreenManager()

    controller = TaskController.load()
    if controller is None:
        controller = TaskController()

    TaskAdventureApp().run()