import random
from typing import Optional


class MessageObject():
    def __init__(self, priority_range: (int, int) ) -> None:
        self.priority=random.randint(priority_range[0], priority_range[1])
        self.initial=self.priority
        self.active=True

    def get_priority(self)-> int:
        return self.priority

    def mark_inactive(self):
        self.active=False

    def is_active(self) -> bool:
        return self.active

    def decrease_key(self,dec: int) -> None:
        if self.priority-dec>0:
            self.priority -= dec


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

    def decrease_key(self,numkeys: int , dec: int) -> None:
        if numkeys<len(self.queue):
            i=0
            while i<numkeys:
                msg=self.queue.pop(0)
                if msg.is_active():
                    msg.decrease_key(dec)
                    self.queue.append(msg)
                    i+=1
        elif len(self.queue)==0:
            return
        else:
            l=len(self.queue)
            for i in range(l):
                msg = self.queue.pop(0)
                if msg.is_active():
                    msg.decrease_key(dec)
                    self.queue.append(msg)

    def decrease_key_dryrun(self,numkeys: int , dec: int) -> list[MessageObject]:
        listout=[]
        if numkeys<len(self.queue):
            i=0
            index=i
            while i<numkeys:
                msg=self.queue[index]
                listout.append(msg)
                if msg.is_active():
                    i+=1
                    index+=1
                else:
                    index+=1
        elif len(self.queue)==0:
            return []
        else:
            return [self.queue]
        return listout






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
        self.next_decrease=[]
        self.priority_queue = PriorityQueue()
        self.age_queue = AgeQueue()
        self.input_interval=int(self.rate_period/self.base_in_rate)
        self.output_interval = int(self.rate_period / self.base_out_rate)
        self.decrease_key_qty, self.decrease_key_period = decrease_key
        self.decrease_key_interval= int(self.rate_period / self.decrease_key_period)

    def gen_next_message(self)->Optional[MessageObject]:
        rate=self.base_in_rate
        if self.surge_in_start<self.timestep<self.surge_in_end:
            rate= self.surge_in_rate
        r=random.randint(1,100)
        if r<=rate:
            priority=random.randint(self.priority_range[0],self.priority_range[1])
            msg=MessageObject(self.priority_range)
            return msg
        return None






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
        # perform decrease
        if len(self.next_decrease)>0:
            self.age_queue.decrease_key(self.decrease_key_qty,1)
            self.next_decrease=[]

        # generate next message in and out one step ahead.
        self.next_incoming=self.gen_next_message()
        # next message out
        if (self.timestep+1)%self.output_interval == 0:
            self.next_outgoing=self.priority_queue.topmessage()
        #next decrease step
        if (self.timestep+1)%self.decrease_key_interval == 0:
            self.next_decrease=self.age_queue.decrease_key_dryrun(self.decrease_key_qty,1)

        self.timestep += 1








if __name__=="__main__":
    x=PriorityQueueProblem(50, 5, 75, 20, 30, (1, 100), (5,30))

    for i in range(200):
        x.do_next_step()

