from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
import priority_queue




class BasicQueue(BoxLayout):
    pass

class PHQueueBox(BoxLayout):
    pass





class MainLayout(Widget):
    priority_queue = ObjectProperty()
    std_height=100
    std_min=25
    curr_height=NumericProperty(100)


    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        self.simulation = priority_queue.PriorityQueueProblem(20, 25, 75, 20, 40, (1, 100), (5,30))

        self.main_row=self.ids.main_row
        self.main_row.add_widget(PHQueueBox())
        self.pqueue=BasicQueue()
        self.main_row.add_widget(self.pqueue)
        self.main_row.add_widget(PHQueueBox())


#    def on_size (self, *args):
#        currhint=min(self.std_height,self.layout.height)
#        if self.layout.height<100:
#            currhint=max(25,self.layout.height)
#        for widget in self.layout.children:
#            widget.maxhint=currhint
#        print(self.layout.height)
    def forward_press(self,*args):
        self.simulation.do_next_step()
        if self.simulation.next_incoming is not None:
            self.pqueue.add_widget(self.simulation.next_incoming.return_vis())


    def backward_press(self, *args):
        self.main_row.add_widget(self.pqueue)


class FibTreeVisApp(App):
    def build(self):
        return MainLayout()


FibTreeVisApp().run()