from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget




class BasicQueue(BoxLayout):
    pass

class QueueBox(BoxLayout):
    labeltext=StringProperty('test')

    def update_label(self,newlable:str)-> None:
        self.labeltext=newlable


class MainLayout(Widget):
    priority_queue = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        layout=self.ids.priority_queue
        for i in range(10):
            this_wid=QueueBox()
            this_wid.update_label(str(i))
            layout.add_widget(this_wid)


class FibTreeVisApp(App):
    def build(self):
        return MainLayout()


FibTreeVisApp().run()