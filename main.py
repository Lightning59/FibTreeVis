from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget




class BasicQueue(BoxLayout):
    pass

class QueueBox(BoxLayout):
    pass

class MainLayout(Widget):
    priority_queue = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        layout=self.ids.priority_queue
        for i in range(50):
            layout.add_widget(QueueBox())


class FibTreeVisApp(App):
    def build(self):
        return MainLayout()


FibTreeVisApp().run()