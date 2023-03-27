import random

class MessageObject():
    def __init__(self, priority_range: (int, int) ) -> None:
        self.priority=random.randint(priority_range[0], priority_range[1])
        self.active=True

    def get_priority(self)-> int:
        return self.priority

    def mark_inactive(self):
        self.active=False

    def is_active(self) -> bool:
        return self.active


class PriorityQueue():

    def __init__(self) -> None:
        self.queue=[]

    def addmessage(self,msg: MessageObject ) -> None:
        if len(self.queue)==0:
            self.queue.append(msg)
        else:
            for i in range(0,len(self.queue)):
                if msg.get_priority()<self.queue[i].get_priority():
                    self.queue.insert(i, msg)
                    return
            self.queue.append(msg)



    def topmessage(self)-> MessageObject:
        if len(self.queue)>0:
            return self.queue[0]
        else:
            return None

    def sendmessage(self)-> MessageObject:
        if len(self.queue)>0:
            return self.queue.pop(0)
        else:
            return None




class AgeQueue():

    def __init__(self) -> None:
        self.queue=[]

    def addmessage(self,msg: MessageObject ) -> None:
        self.queue.append(msg)





class PriorityQueueProblem():

    def __init__(self, base_in_rate: int, base_out_rate: int, surge_in_rate: int, surge_in_start: int,
                 surge_in_end: int, priority_range: (int, int), decrease_key:(int, int)) -> None:

        self.base_in_rate=base_in_rate
        self.base_out_rate=base_out_rate
        self.surge_in_rate = surge_in_rate
        self.surge_in_start = surge_in_start
        self.surge_in_end = surge_in_end
        self.timestep=0
        self.rate_period = 100
        self.priority_range = priority_range
        self.next_incoming = None
        self.next_outgoing = None
        self.priority_queue = PriorityQueue()
        self.age_queue = AgeQueue()
        self.input_interval=int(self.rate_period/self.base_in_rate)
        self.output_interval = int(self.rate_period / self.base_out_rate)
        self.decrease_key_qty, self.decrease_key_period = decrease_key
        self.decrease_key_interval= int(self.rate_period / self.decrease_key_period)


    def do_next_step(self) -> None:
        # add incoming messages to queue and reset incoming queue
        if self.next_incoming is not None:
            self.priority_queue.addmessage(self.next_incoming)
            self.age_queue.addmessage(self.next_incoming)
            self.next_incoming=None
        # send outgoing messages reset outgoint mark message in time queue as inactive
        if self.next_outgoing is not None:
            msg=self.priority_queue.sendmessage()
            msg.mark_inactive()
            self.next_outgoing = None

        # generate next message in and out one step ahead.
        if (self.timestep+1)%self.input_interval == 0:
            self.next_incoming=MessageObject(self.priority_range)
        # next message out
        if (self.timestep+1)%self.output_interval == 0:
            self.next_outgoing=self.priority_queue.topmessage()

        self.timestep += 1








if __name__=="__main__":
    x=PriorityQueueProblem(50, 5, 75, 20, 30, (1, 100), (5,30))

    for i in range(200):
        x.do_next_step()

