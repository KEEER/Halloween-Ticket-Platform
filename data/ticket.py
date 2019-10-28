import uuid
import pickle
class  Ticket:
    def __init__(self, bought_time, start_time, expired):
        self.id = str(uuid.uuid1())
        self.bought_time = bought_time
        self.start_time = start_time

