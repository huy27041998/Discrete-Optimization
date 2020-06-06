from PriorityQueue import PriorityQueue
import numpy as np

pq = PriorityQueue()
a  = np.array([[1, 2, 3, 4], [5, 6, 7, 0]])
a1 = np.array([[1, 2, 3, 4], [5, 6, 7, -7/2]])
a2 = np.array([[1, 2, 3, 4], [5, 6, 7, 35]])
a3 = np.array([[1, 2, 3, 4], [5, 6, 7, 4]])
pq.push(a, a[-1, -1])
pq.push(a1, a1[-1, -1])
# pq.push(a2, a2[-1, -1])
# pq.push(a3, a3[-1, -1])
print(pq.pop())