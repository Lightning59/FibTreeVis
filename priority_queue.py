import random
from typing import Optional

from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ColorProperty
from kivy.uix.boxlayout import BoxLayout


class QueueBox(BoxLayout):
    initial_label = StringProperty('init')
    curr_label = StringProperty('curr')
    time_label = StringProperty('Age: 0')
    max_hint = NumericProperty(100)
    active=BooleanProperty(True)
    active_color = ColorProperty([1,.6,0,1])


    def __init__(self, val: int, **kwargs) -> None:
        super(QueueBox, self).__init__(**kwargs)
        self.initial_label = str(val)
        self.curr_label = str(val)

    def update_curr(self, val: int) -> None:
        self.curr_label = str(val)

    def update_time(self, val: int) -> None:
        self.time_label = "Age: "+str(val)

    def mark_inactive(self):
        self.active=False
        self.active_color=[.4,.4,.4,1]

    def on_size(self, *args) -> None:
        try:
            current_hint = min(100, self.parent.height)
            if self.parent.height < 100:
                current_hint = max(25, self.parent.height)
            self.max_hint = current_hint
        except AttributeError:
            self.max_hint = 100


class MessageObject:
    def __init__(self, priority_range: tuple[int, int]) -> None:
        self.time_label=0
        self.priority = random.randint(priority_range[0], priority_range[1])
        self.initial = self.priority
        self.still_active = True
        self.vis_incoming = QueueBox(self.priority)
        self.vis_pq = QueueBox(self.priority)
        self.vis_outgoing = QueueBox(self.priority)
        self.vis_aq= QueueBox(self.priority)
        self.vis_dk = QueueBox(self.priority)
        self.vis_list=[self.vis_incoming,self.vis_pq,self.vis_outgoing,self.vis_aq,self.vis_dk]

    def increment_time(self):
        self.time_label+=1
        for vis in self.vis_list:
            vis.update_time(self.time_label)

    def get_priority(self) -> int:
        return self.priority

    def mark_inactive(self) -> None:
        self.still_active=False
        for vis in self.vis_list:
            vis.mark_inactive()

    def is_active(self) -> bool:
        return self.still_active

    def decrease_key(self, dec: int) -> None:
        if self.priority - dec > 0:
            self.priority -= dec
            for vis in self.vis_list:
                vis.update_curr(self.priority)

    def return_vis(self, application: int) -> Optional[QueueBox]:
        if application == 0:
            return self.vis_incoming
        elif application ==1:
            return self.vis_pq
        elif application ==2:
            return self.vis_outgoing
        elif application ==3:
            return self.vis_aq
        elif application ==4:
            return self.vis_dk
        else:
            return None



class PriorityQueue:

    def __init__(self) -> None:
        self.queue = []

    def add_message(self, msg: MessageObject) -> None:
        if len(self.queue) == 0:
            self.queue.append(msg)
        else:
            for i in range(0, len(self.queue)):
                if msg.get_priority() < self.queue[i].get_priority():
                    self.queue.insert(i, msg)
                    return
            self.queue.append(msg)

    def top_message(self) -> Optional[MessageObject]:
        if len(self.queue) > 0:
            return self.queue[0]
        else:
            return None

    def send_message(self) -> Optional[MessageObject]:
        if len(self.queue) > 0:
            return self.queue.pop(0)
        else:
            return None

    def decrease_key_update(self):
        self.queue.sort(key=lambda obj: obj.get_priority())

class AgeQueue:

    def __init__(self) -> None:
        self.queue = []

    def add_message(self, msg: MessageObject) -> None:
        self.queue.append(msg)

    def decrease_key(self, num_keys: int, dec: int) -> None:
        if num_keys < len(self.queue):
            i = 0
            while i < num_keys:
                msg = self.queue.pop(0)
                if msg.is_active():
                    msg.decrease_key(dec)
                    self.queue.append(msg)
                    i += 1
        elif len(self.queue) == 0:
            return
        else:
            queue_len = len(self.queue)
            for i in range(queue_len):
                msg = self.queue.pop(0)
                if msg.is_active():
                    msg.decrease_key(dec)
                    self.queue.append(msg)

    def decrease_key_dryrun(self, num_keys: int) -> list[MessageObject]:
        list_out = []
        if num_keys < len(self.queue):
            i = 0
            index = i
            while i < num_keys:
                msg = self.queue[index]
                list_out.append(msg)
                if msg.is_active():
                    i += 1
                    index += 1
                else:
                    index += 1
        elif len(self.queue) == 0:
            return []
        else:
            return self.queue
        return list_out


class PriorityQueueProblem:

    def __init__(self, base_in_rate: int, base_out_rate: int, surge_in_rate: int, surge_in_start: int,
                 surge_in_end: int, priority_range: tuple[int, int], decrease_key: tuple[int, int]) -> None:
        """
        Class constructor for a priority queue simulation
        :param base_in_rate: number of packages in per base rate that come in on avg (currently base rate is 100 steps)
        :param base_out_rate: number of packages sent per base rate that come in on avg (currently base rate is 100
        steps)
        :param surge_in_rate: number of packages in per base rate during an elevated surge period that come in on avg
        (currently base rate is 100 steps)
        :param surge_in_start: how many steps in till surge begins
        :param surge_in_end: how many steps from beginning till surge ends
        :param priority_range: tuple of two ints lowest and highest possible priority (uniform randomly assigned)
        :param decrease_key: (number of messages to reduce at time, Rate in times per 100 which this will occur)
        """

        self.base_in_rate = base_in_rate
        self.base_out_rate = base_out_rate
        self.surge_in_rate = surge_in_rate
        self.surge_in_start = surge_in_start
        self.surge_in_end = surge_in_end
        self.timestep = 0
        self.rate_period = 100
        self.priority_range = priority_range
        self.next_incoming = None
        self.next_outgoing = None
        self.next_decrease = []
        self.priority_queue = PriorityQueue()
        self.age_queue = AgeQueue()
        self.input_interval = int(self.rate_period / self.base_in_rate)
        self.output_interval = int(self.rate_period / self.base_out_rate)
        self.decrease_key_qty, self.decrease_key_period = decrease_key
        self.decrease_key_interval = int(self.rate_period / self.decrease_key_period)

    def gen_next_message(self) -> Optional[MessageObject]:
        rate = self.base_in_rate
        if self.surge_in_start < self.timestep < self.surge_in_end:
            rate = self.surge_in_rate
        r = random.randint(1, 100)
        if r <= rate:
            msg = MessageObject(self.priority_range)
            return msg
        return None

    def do_next_step(self) -> None:
        # add incoming messages to queue and reset incoming queue
        if self.next_incoming is not None:
            self.priority_queue.add_message(self.next_incoming)
            self.age_queue.add_message(self.next_incoming)
            self.next_incoming = None
        # send outgoing messages reset outgoing mark message in time queue as inactive
        if self.next_outgoing is not None:
            msg = self.priority_queue.send_message()
            msg.mark_inactive()
            self.next_outgoing = None
        # perform decrease
        if len(self.next_decrease) > 0:
            self.age_queue.decrease_key(self.decrease_key_qty, 1)
            self.next_decrease = []
            self.priority_queue.decrease_key_update()

        # generate next message in and out one step ahead.
        self.next_incoming = self.gen_next_message()
        # next message out
        if (self.timestep + 1) % self.output_interval == 0:
            self.next_outgoing = self.priority_queue.top_message()
        # next decrease step
        if (self.timestep + 1) % self.decrease_key_interval == 0:
            self.next_decrease = self.age_queue.decrease_key_dryrun(self.decrease_key_qty)

        self.timestep += 1
        for message in self.priority_queue.queue:
            message.increment_time()


if __name__ == "__main__":
    x = PriorityQueueProblem(50, 5, 75, 20, 30, (1, 100), (5, 30))

    for trial_step in range(200):
        x.do_next_step()
