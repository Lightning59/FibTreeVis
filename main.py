from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
import priority_queue


class BasicQueue(BoxLayout):
    pass


class PHQueueBox(BoxLayout):
    pass


class MainLayout(Widget):
    main_row: BoxLayout
    age_row: BoxLayout
    priority_queue = ObjectProperty()
    std_height = 100
    std_min = 25
    curr_height = NumericProperty(100)
    curr_step=StringProperty("0")

    def __init__(self, **kwargs) -> None:
        super(MainLayout, self).__init__(**kwargs)

        self.simulation = priority_queue.PriorityQueueProblem(20, 25, 50, 20, 100, (1, 100), (5, 15))
        self.main_row = self.ids.main_row
        self.age_row = self.ids.age_row
        self.main_row.add_widget(PHQueueBox())
        self.pqueue = BasicQueue()
        self.main_row.add_widget(self.pqueue)
        self.main_row.add_widget(PHQueueBox())
        self.age_queue=BasicQueue()
        self.next_decrease=BasicQueue()
        self.age_row.add_widget(self.age_queue)
        self.age_row.add_widget(self.next_decrease)

    #    def on_size (self, *args):
    #        pass

    def remove_all_children(self,boxlayout:BoxLayout)->None:
        children = boxlayout.children.copy()
        for child in children:
            boxlayout.remove_widget(child)

    def update_priority_queue_display(self):
        self.remove_all_children(self.pqueue)
        msg: priority_queue.MessageObject
        msglist= self.simulation.priority_queue.queue[::-1]

        for msg in msglist:
            self.pqueue.add_widget(msg.return_vis(1))

    def update_main_row(self):
        self.remove_all_children(self.main_row)

        if self.simulation.next_incoming is not None:
            self.main_row.add_widget(self.simulation.next_incoming.return_vis(0))
        else:
            self.main_row.add_widget(PHQueueBox())

        self.main_row.add_widget(self.pqueue)
        self.update_priority_queue_display()

        if self.simulation.next_outgoing is not None:
            self.main_row.add_widget(self.simulation.next_outgoing.return_vis(2))
        else:
            self.main_row.add_widget(PHQueueBox())

    def update_age_queue_display(self):
        self.remove_all_children(self.age_queue)
        msg: priority_queue.MessageObject
        msglist = self.simulation.age_queue.queue[::-1]
        for msg in msglist:
            self.age_queue.add_widget(msg.return_vis(3))

    def update_decrease_key_display(self):
        self.remove_all_children(self.next_decrease)
        msg: priority_queue.MessageObject
        msglist = self.simulation.next_decrease[::-1]
        for msg in msglist:
            self.next_decrease.add_widget(msg.return_vis(4))

    def update_age_row(self):
        self.update_age_queue_display()
        self.update_decrease_key_display()


    def forward_press(self, *args) -> None:
        self.simulation.do_next_step()
        self.update_main_row()
        self.update_age_row()
        self.curr_step=str(self.simulation.timestep)

    def backward_press(self, *args) -> None:
        self.main_row.add_widget(self.pqueue)


class FibTreeVisApp(App):
    def build(self) -> MainLayout:
        return MainLayout()


FibTreeVisApp().run()
