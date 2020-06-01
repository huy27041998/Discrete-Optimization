from collections import deque, namedtuple
Node = namedtuple('Node', ['level', 'weight', 'value', 'items'])
class KnapsackSolver:
    def __init__(self, item_count, items, capacity):
        super().__init__()
        self.item_count = item_count
        self.items = items
        self.capacity = capacity
    def search(self):
        self.pq = deque([])
        v = Node(-1, 0, 0, [])
        self.pq.append(v)
        maxValue = 0
        bestItems = []
        while(len(self.pq) != 0):
            v = self.pq[0]
            self.pq.popleft()
            u1 = Node(v.level + 1, v.weight + self.items[v.level+1].weight, v.value + self.items[v.level+1].value, v.items)
            u1.items.append(self.items[u1.level].index)
            u2 = Node(v.level + 1, v.weight, v.value, v.items)
            if (u1.weight <= self.capacity and u1.value > maxValue):
                maxValue = u1.value
                bestItems = u1.items
            self.compute_bound(u1, maxValue)
            self.compute_bound(u2, maxValue)
        taken = [0] * len(self.items)
        for i in range(len(bestItems)):
            taken[bestItems[i]] = 1
        return maxValue, taken
    def compute_bound(self, u, maxValue):
        if(u.weight >= self.capacity):
            return 0
        else:
            bound = u.value
            j = u.level + 1
            totweight = u.weight

            while(j < self.item_count and totweight + self.items[j].weight <= self.capacity):
                totweight += self.items[j].weight
                bound += self.items[j].value
                j = j + 1
            k = j
            if(k <= self.item_count - 1):
                bound = bound + (self.capacity - totweight)*self.items[k].value / self.items[k].weight

        if (bound > maxValue):
            self.pq.append(u)


    
    