from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

class TaskAdventure(Screen):
    pass

class AddTaskDialog(Screen):

    title = ObjectProperty(None)
    description = ObjectProperty(None)

    def save(self):
        print("SAVE: " + self.title.text + " : " + self.description.text)

    def cancel(self):
        print("CANCEL")

class WaitTaskDialog(Screen):
    pass

class RunningTaskDialog(Screen):
    pass



class TaskAdventureApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WaitTaskDialog(name='wait_task'))
        sm.add_widget(AddTaskDialog(name='add_task'))
        sm.add_widget(RunningTaskDialog(name='run_task'))
        return sm

if __name__ == '__main__':
    TaskAdventureApp().run()