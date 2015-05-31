from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

from tasks import TaskController


class TaskAdventure(Widget):
    pass


class AddTaskDialog(Screen):

    title = ObjectProperty(None)
    description = ObjectProperty(None)

    def save(self):
        print("SAVE: " + self.title.text + ", " + self.description.text)

        title = self.title.text.strip().replace("\t", " ")
        description = self.description.text.strip().replace("\t", " ")

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
            """@TODO: add pop up for notify user about empty database"""


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
            # @TODO: add message

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
                """@TODO: Add pop up window with question about task status"""

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