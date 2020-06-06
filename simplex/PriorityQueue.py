import heapq
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)
    
    def empty(self):
        if (len(self._queue) is 0):
            return True
        else:
            return False
    
    def length(self):
        return len(self._queue)