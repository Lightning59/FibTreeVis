

class PriorityQueue():

    def __init__(self):
        self.queue=[]


class AgeQueue():

    def __init__(self):
        self.queue=[]

class PriorityQueueProblem():

    def __init__(self, base_in_rate: int, base_out_rate: int, surge_in_rate: int, surge_in_start: int,
                 surge_in_end: int) -> None:
        self.base_in_rate=base_in_rate
        self.base_out_rate=base_out_rate
        self.surge_in_rate = surge_in_rate
        self.surge_in_start = surge_in_start
        self.surge_in_end = surge_in_end
        self.timestep=0
        self.rate_period = 100





if __name__=="__main__":
    x=PriorityQueueProblem(5,10,15,20,30)
