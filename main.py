from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget




class BasicQueue(BoxLayout):
    pass

class QueueBox(BoxLayout):
    initial_label=StringProperty('init')
    curr_label = StringProperty('curr')
    maxhint = NumericProperty(100)

    def on_size(self, *args):
        try:
            currhint = min(100, self.parent.height)
            if self.parent.height < 100:
                currhint = max(25, self.parent.height)
            self.maxhint = currhint
        except AttributeError:
            self.maxhint=100


class MainLayout(Widget):
    priority_queue = ObjectProperty()
    std_height=100
    std_min=25
    curr_height=NumericProperty(100)

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)
        self.layout=self.ids.priority_queue
        for i in range(10):
            this_wid=QueueBox()
            this_wid.initial_label=str(i)
            this_wid.curr_label=str(i-1)
            self.layout.add_widget(this_wid)

#    def on_size (self, *args):
#        currhint=min(self.std_height,self.layout.height)
#        if self.layout.height<100:
#            currhint=max(25,self.layout.height)
#        for widget in self.layout.children:
#            widget.maxhint=currhint
#        print(self.layout.height)


class FibTreeVisApp(App):
    def build(self):
        return MainLayout()


FibTreeVisApp().run()