from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget




class BasicQueue(BoxLayout):
    pass

class PHQueueBox(BoxLayout):
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
        self.main_row=self.ids.main_row
        self.main_row.add_widget(PHQueueBox())
        self.pqueue=BasicQueue()
        self.main_row.add_widget(self.pqueue)
        self.main_row.add_widget(PHQueueBox())
        for i in range(10):
            this_wid=QueueBox()
            this_wid.initial_label=str(i)
            this_wid.curr_label=str(i-1)
            self.pqueue.add_widget(this_wid)

#    def on_size (self, *args):
#        currhint=min(self.std_height,self.layout.height)
#        if self.layout.height<100:
#            currhint=max(25,self.layout.height)
#        for widget in self.layout.children:
#            widget.maxhint=currhint
#        print(self.layout.height)
    def forward_press(self,*args):
        print(self.main_row.children)
        if __name__ == '__main__':
            childlist=self.main_row.children.copy()
        for child in range(len(childlist)):
            if __name__ == '__main__':
                self.main_row.remove_widget(childlist[child])
        print("pressed")

    def backward_press(self, *args):
        self.main_row.add_widget(self.pqueue)


class FibTreeVisApp(App):
    def build(self):
        return MainLayout()


FibTreeVisApp().run()