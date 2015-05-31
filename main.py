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


class TaskAdventure(Widget):
    pass


class AddTaskDialog(Screen):

    title = ObjectProperty(None)
    description = ObjectProperty(None)

    def save(self):

        title = self.title.text.strip().replace("\t", " ")
        description = self.description.text.strip().replace("\t", " ")

        if len(title) == 0:
            popup = Popup(title='Empty Title',
                          content=Label(text="New task can't be empty."),
                          size_hint=(0.8, 0.3))
            popup.open()
            return False

        controller.services.add_task(title, description)
        controller.save()

        self.title.text = self.description.text = ""

        sm.transition.direction = 'left'

        if controller.status is False:
            sm.current = "wait_task"
        else:
            sm.current = "run_task"

    def cancel(self):
        self.title.text = self.description.text = ""

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

            sm.transition.direction = 'right'
            sm.current = "run_task"
        else:
            popup = Popup(title='Empty Database',
                          content=Label(text='Database is empty. Please add few tasks manually.'),
                          size_hint=(0.8, 0.3))
            popup.open()



class RunningTaskDialog(Screen):

    title = ObjectProperty(None)
    description = ObjectProperty(None)
    clock = ObjectProperty(None)

    def on_pre_enter(self, *args):
        self.update()
        self.title.text = str(controller.services.running_task.title)
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

            sm.transition.direction = 'down'
            sm.current = "wait_task"
        else:
            self.clock.text = str(controller.time_left()).split(".")[0]


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