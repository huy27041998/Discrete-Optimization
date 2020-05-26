from itertools import combinations
from time import time
import math
from collections import namedtuple
import random
Point = namedtuple("Point", ['x', 'y'])
class TwoOptSolver():
    def __init__(self, cycle, nodeCount, points):
        self.cycle = cycle
        self.nodeCount = nodeCount
        self.points = points
        self.CMP_THRESHOLD = 3
        self.abc = False
        self.obj = self.calculate_obj()
    def calculate_obj(self):
        return sum([self.edge_length(i, i+1) for i in range(self.nodeCount - 1)]) + self.edge_length(self.nodeCount-1, 0)
    def edge_length(self, idx1, idx2, ):
        point1, point2 = self.points[self.cycle[idx1]], self.points[self.cycle[idx2]]
        return length(point1, point2)
    def swap(self, start, end):
        self.abc = True
        improved = False
        new_cycle = self.cycle[:start] + self.cycle[start:end+1][::-1] + self.cycle[end + 1:]
        with open('debug.txt', 'w') as f:
            f.write(str(self.cycle) + '\n')
            f.write(str(new_cycle))
        # print(self.cycle[start-1], self.cycle[start]  , -self.edge_length(self.cycle[start-1], self.cycle[start]   ))
        # print(self.cycle[end]    , self.cycle[end+1]  , -self.edge_length(self.cycle[end]    , self.cycle[end+1]   ))
        # print(self.cycle[start]  , self.cycle[start+1], -self.edge_length(self.cycle[start]  , self.cycle[start+1] ))
        # print(self.cycle[end-1]  , self.cycle[end]    , -self.edge_length(self.cycle[end-1]  , self.cycle[end]     ))
        # print(new_cycle[start - 1], new_cycle[start]  , +self.edge_length(new_cycle[start - 1], new_cycle[start]   ))
        # print(new_cycle[end]      , new_cycle[end+1]  , +self.edge_length(new_cycle[end]      , new_cycle[end+1]   ))
        # print(new_cycle[start]    , new_cycle[start+1], +self.edge_length(new_cycle[start]    , new_cycle[start+1] ))
        # print(new_cycle[end - 1]  , new_cycle[end]    , +self.edge_length(new_cycle[end - 1]  , new_cycle[end]     ))
            
        new_obj = self.obj - \
            (self.edge_length(self.cycle[start-1], self.cycle[start]) + \
            self.edge_length(self.cycle[end], self.cycle[end+1])) + \
            (self.edge_length(new_cycle[start - 1], new_cycle[start])) + \
            self.edge_length(new_cycle[end], new_cycle[end+1])
        print(new_obj - self.obj)
        print('\n\n\n')
        if new_obj < self.obj - self.CMP_THRESHOLD:
            # self.cycle = new_cycle
            self.obj = new_obj
            improved = True
        return improved
    def solve(self, t_threshold=None):
        improved = True
        t = time()
        while improved:
            if t_threshold and time() - t >= t_threshold:
                break
            improved = False
            for start, end in combinations(range(1, len(self.cycle) - 1), 2):
                if self.swap(start, end):
                    improved = True
                    break
        return self
def readData(file_location):
    with open(file_location, 'r') as input_data_file:
        input_data = input_data_file.read()
    lines = input_data.split('\n')
    nodeCount = int(lines[0])
    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    return nodeCount, points

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def getLength(i, j, cur_solution, points, nodeCount, i0, j0):
    if i == nodeCount:
        i = 0
    if j == nodeCount:
        j = 0
    if i == -1:
        i = nodeCount - 1
    if j == -1:
        j = nodeCount - 1
    # print(cur_solution[i], cur_solution[j], length(points[cur_solution[i]], points[cur_solution[j]]))
    return length(points[cur_solution[i]], points[cur_solution[j]])

def getSwapDelta(i, j, cur_solution, points, nodeCount):
    delta = 0.0
    # print(i  , i+1, cur_solution[i  ], cur_solution[i+1], - getLength(i  , i+1, cur_solution, points, nodeCount, i, j))
    # print(j  , j+1, cur_solution[j  ], cur_solution[j+1], - getLength(j  , j+1, cur_solution, points, nodeCount, i, j))
    # print(i  , j  , cur_solution[i  ], cur_solution[j  ], + getLength(i  , j  , cur_solution, points, nodeCount, i, j))
    # print(i+1, j+1, cur_solution[i+1], cur_solution[j+1], + getLength(i+1, j+1, cur_solution, points, nodeCount, i, j))
    delta += \
        - getLength(i, i+1, cur_solution, points, nodeCount, i, j) \
        - getLength(j, j+1, cur_solution, points, nodeCount, i, j) \
        + getLength(i, j, cur_solution, points, nodeCount, i, j) \
        + getLength(i+1, j+1, cur_solution, points, nodeCount, i, j)
    return delta

def swapValuePropagate(i, j, cur_solution, points, cur_obj, nodeCount, delta):
    obj = cur_obj + delta
    new_solution = cur_solution.copy()
    if i < j:
        new_solution = new_solution[:i+1] + new_solution[i+1:j+1][::-1] + new_solution[j+1:]
    else:
        new_solution = new_solution[:j+1] + new_solution[j+1:i+1][::-1] + new_solution[i+1:]
    return new_solution, obj

def calculate_obj(solution, points, nodeCount):
    return sum([length(points[solution[i]], points[solution[i+1]]) for i in range(nodeCount - 1)]) + length(points[solution[nodeCount-1]], points[solution[0]])

def getMultiSwapDelta(cur_solution, points, nodeCount, swapList, cur_obj):
    new_solution = cur_solution.copy()
    delta = 0
    obj = cur_obj
    for i, j in swapList:
        delta_temp = getSwapDelta(i, j, new_solution, points, nodeCount)
        delta += delta_temp
        new_solution, obj = swapValuePropagate(i, j, new_solution, points, obj, nodeCount, delta_temp)
    return delta, new_solution

def swapMultiValuePropagate(delta, cur_obj, new_solution):
    new_obj = cur_obj + delta
    return new_solution, new_obj

def getNeighborhood(nodeCount, k, list_size=1):
    # randomly get k neiborhood from cur_solution
    neighborhoods = []
    if k == -1:
        neighborhood = []
        # get all pairs of node
        for i in range(nodeCount-1):
            for j in range(i+1, nodeCount-1):
                    neighborhood.append((i, j))
        random.shuffle(neighborhood)
        return neighborhood
    for i in range(list_size):
        neighborhood = []
        node = [i for i in range(nodeCount)]
        while(len(neighborhood) < k):
            idx1 = random.randint(0, len(node) - 1)
            n1 = node[idx1]
            node.pop(idx1)
            idx2 = random.randint(0, len(node) - 1)
            n2 = node[idx2]
            node.pop(idx2)
            neighborhood.append((n1, n2))
        neighborhoods.append(neighborhood)
    return neighborhoods


nodeCount, points = readData("data/tsp_280_1")
t = TwoOptSolver([99, 67, 80, 132, 149, 235, 51, 9, 134, 68, 21, 141, 198, 113, 226, 31, 212, 175, 28, 171, 71, 109, 206, 121, 53, 74, 250, 159, 148, 47, 118, 57, 278, 194, 244, 84, 92, 261, 3, 153, 115, 87, 15, 274, 277, 117, 138, 146, 270, 13, 210, 195, 16, 73, 272, 276, 266, 216, 66, 241, 157, 225, 183, 127, 48, 254, 30, 176, 137, 46, 63, 70, 230, 263, 229, 224, 246, 88, 258, 231, 94, 242, 172, 130, 160, 18, 19, 158, 135, 25, 83, 173, 239, 55, 105, 114, 213, 265, 90, 2, 249, 197, 151, 240, 24, 23, 238, 211, 144, 185, 253, 52, 162, 245, 60, 98, 220, 131, 116, 152, 196, 168, 193, 207, 96, 262, 119, 178, 20, 184, 62, 237, 177, 203, 205, 234, 85, 182, 142, 11, 4, 174, 218, 128, 214, 78, 69, 221, 179, 36, 271, 40, 49, 143, 208, 106, 243, 110, 41, 252, 169, 188, 5, 150, 227, 120, 165, 273, 103, 38, 215, 222, 202, 42, 76, 154, 125, 17, 34, 107, 268, 93, 75, 170, 129, 61, 201, 217, 166, 228, 59, 8, 126, 164, 259, 251, 191, 145, 223, 111, 65, 209, 156, 100, 275, 50, 256, 247, 82, 260, 7, 267, 232, 89, 189, 32, 91, 35, 12, 29, 79, 123, 155, 190, 112, 199, 192, 81, 45, 102, 39, 1, 236, 108, 248, 187, 200, 163, 186, 122, 43, 64, 22, 95, 33, 133, 139, 181, 257, 124, 279, 97, 104, 86, 136, 44, 14, 26, 264, 180, 167, 6, 140, 204, 37, 72, 219, 255, 77, 147, 101, 161, 10, 58, 269, 56, 233, 27, 54, 0], nodeCount, points)
cur_obj = t.calculate_obj()

#test swap 2 value
# i = 58
# j = 80
# delta = getSwapDelta(i, j, t.cycle, points, nodeCount)
# new_solution, new_obj = swapValuePropagate(i, j, t.cycle, points, cur_obj, nodeCount, delta)
# print(t.cycle)
# print(new_solution)
# print(cur_obj, delta, new_obj, calculate_obj(new_solution, points, nodeCount))

#test swap k value

swap_lists = getNeighborhood(nodeCount, 20, 1000)
for swap_list in swap_lists:
    delta, new_solution = getMultiSwapDelta(t.cycle, points, nodeCount, swap_list, cur_obj)
    # print(delta, cur_obj + delta, calculate_obj(new_solution, points, nodeCount))
    print(math.fabs(cur_obj + delta - calculate_obj(new_solution, points, nodeCount)) < 1e-3, swap_list)

# swap_list = [(235, 26), (161, 215), (80, 206), (227, 10), (131, 183), (186, 94), (72, 110), (6, 48), (157, 80), (244, 253), (108, 123), (184, 154), (87, 128), (25, 44), (64, 215), (198, 72), (14, 22), (10, 216), (92, 92), (102, 6)]
# delta, new_solution = getMultiSwapDelta(t.cycle, points, nodeCount, swap_list, cur_obj)
# print(delta, cur_obj + delta, calculate_obj(new_solution, points, nodeCount))
