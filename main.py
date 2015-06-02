from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.button import Button

from tasks import TaskController

__version__ = "1.0"


class TaskAdventure(Widget):
    pass


class AddTaskDialog(Screen):

    description = ObjectProperty(None)

    def save(self):

        description = self.description.text.strip().replace("\t", " ")

        if len(description) == 0:
            popup = Popup(title='Empty Task',
                          content=Label(text="Task can't be empty."),
                          size_hint=(0.8, 0.3))
            popup.open()
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

    def start(self):
        print("START")

        ret = controller.services.start_random_task()
        if ret is True:
            controller.status = True
            controller.save()

            sm.transition.direction = 'up'
            sm.current = "run_task"
        else:
            popup = Popup(title='Empty Database',
                          content=Label(text='Please, add few tasks manually.'),
                          size_hint=(0.8, 0.3))
            popup.open()



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

            # @TODO: add 2 buttons for answer and what?!
            # if Yes - then clear running_task
            # if No - then what?!

            popup = Popup(title='Time out',
                          content=Label(text='Do you complete task'),
                          size_hint=(0.8, 0.3))
            popup.open()

            controller.status = controller.is_running_task()
            controller.services.running_task = None

            controller.save()

            sm.transition.direction = 'down'
            sm.current = "wait_task"
        else:
            self.clock.text = str(controller.time_left()).split(".")[0]  # remove milliseconds


class TaskAdventureApp(App):

    def build(self):

        sm.add_widget(WaitTaskDialog(name='wait_task'))
        sm.add_widget(AddTaskDialog(name='add_task'))
        sm.add_widget(RunningTaskDialog(name='run_task'))

        sm.transition.direction = 'up'

        controller.status = controller.is_running_task()

        if controller.status is False:
            if controller.services.running_task is None:
                sm.current = 'wait_task'
            else:
                # @TODO: Add pop up window with question about task status
                # see early
                popup = Popup(title='Time out',
                          content=Label(text='Do you complete task'),
                          size_hint=(0.8, 0.3))
                popup.open()

                controller.services.running_task = None

                controller.save()

                sm.current = 'wait_task'

        else:
            sm.current = 'run_task'

        return sm


if __name__ == '__main__':

    sm = ScreenManager()

    controller = TaskController.load()
    if controller is None:
        controller = TaskController()

    TaskAdventureApp().run()