import heapq
class PriorityQueue:
    def __init__(self):
        super().__init__()
        self.queue = []
        self.len = 0
    def push(self, item, priority):
        heapq.heappush(self.queue, (-priority, self.len, item))
        self.len += 1

    def pop(self):
        self.len -= 1
        return heapq.heappop(self.queue)[-1]
    
    def empty(self):
        return self.len == 0
    
    def length(self):
        return len(self.queue)   