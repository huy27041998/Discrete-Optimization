import random
from collections import namedtuple
import math
from tqdm import tqdm
Point = namedtuple("Point", ['x', 'y'])
Swap = namedtuple("Swapmove", ['i', 'j', 'delta'])
Multiswap = namedtuple("Multiswapmove", ['delta', 'solution'])
_print = False
class Tsp:
    def __init__(self, nodeCount, points):
        self.nodeCount = nodeCount
        self.points = points
        self._print = False
    
    def calculate_obj(self):
        solution = self.solution
        return sum([length(points[solution[i]], points[solution[i+1]]) for i in range(nodeCount - 1)]) + length(points[solution[nodeCount-1]], points[solution[0]])

    def generateInitialSolution(self):
        L = [i for i in range(self.nodeCount)]
        obj = 0
        inititalSolution = []
        for i in range(nodeCount):
            index = random.randint(0, len(L) - 1)
            inititalSolution.append(L[index])
            if (i > 0):
                obj += length(points[inititalSolution[i]], points[inititalSolution[i-1]])
            L.pop(index)
        obj += length(points[inititalSolution[nodeCount-1]], points[inititalSolution[0]])
        if _print: print('Initial solution', inititalSolution, 'current obj = ', obj)
        self.solution = inititalSolution
        self.obj = obj

    def getLength(self, i, j, i0, j0):
        if i == self.nodeCount:
            i = 0
        if j == self.nodeCount:
            j = 0
        if i == -1:
            i = self.nodeCount - 1
        if j == -1:
            j = self.nodeCount - 1
        return length(points[self.solution[i]], points[self.solution[j]])

    def getSwapDelta(self, i, j):
        delta = 0.0
        delta += \
            - self.getLength(i  , i+1, i, j) \
            - self.getLength(j  , j+1, i, j) \
            + self.getLength(i  , j  , i, j) \
            + self.getLength(i+1, j+1, i, j)
        return delta
    
    def getMultiSwapDelta(self, swapList):
        def getLength(i, j, cur_solution, points, nodeCount, i0, j0):
            if i == nodeCount:
                i = 0
            if j == nodeCount:
                j = 0
            if i == -1:
                i = nodeCount - 1
            if j == -1:
                j = nodeCount - 1
            return length(points[cur_solution[i]], points[cur_solution[j]])

        def getSwapDelta(i, j, cur_solution, points, nodeCount):
            delta = 0.0
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
        
        new_solution = self.solution.copy()
        delta = 0
        obj = self.obj
        for i, j in swapList:
            delta_temp = getSwapDelta(i, j, new_solution, points, nodeCount)
            delta += delta_temp
            new_solution, obj = swapValuePropagate(i, j, new_solution, points, obj, nodeCount, delta_temp)
        return delta, new_solution

    def swapValuePropagate(self, candidate):
        obj = self.obj + candidate.delta
        new_solution = self.solution.copy()
        i = candidate.i
        j = candidate.j
        if i < j:
            new_solution = new_solution[:i+1] + new_solution[i+1:j+1][::-1] + new_solution[j+1:]
        else:
            new_solution = new_solution[:j+1] + new_solution[j+1:i+1][::-1] + new_solution[i+1:]
        return new_solution, obj

    def swapMultiValuePropagate(self, candidate):
        self.obj += candidate.delta
        self.solution = candidate.solution
    
    def getNeighborhood(self, k, list_size=None):
        neighborhoods = []
        if k == -1:
            neighborhood = []
            # get all pairs of node
            for i in range(self.nodeCount-1):
                for j in range(i+1, self.nodeCount-1):
                        neighborhood.append((i, j))
            random.shuffle(neighborhood)
            return neighborhood
        for i in range(list_size):
            neighborhood = []
            node = [i for i in range(self.nodeCount)]
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

    def hillclimbingsearch(self, maxIter):
        self.generateInitialSolution()
        for it in tqdm(range(maxIter)):
            it += 1
            candidate = []
            swap_list = self.getNeighborhood(k=-1)
            best_delta = 0
            for i, j in swap_list:
                delta = self.getSwapDelta(i, j)
                if delta < best_delta:
                    best_delta = delta
                    candidate = []
                    candidate.append(Swap(i, j, delta))
                elif delta < 0 and delta == best_delta:
                    candidate.append(Swap(i, j, delta))
            if len(candidate) == 0:
                if self._print: print('Reach local optimum')
                break
            index = random.randint(0, len(candidate) - 1)
            self.swapValuePropagate(candidate[index])
            if self._print: print('Step ' + str(it) + ': current obj = ' + str(self.obj) +  ', True obj = ', self.calculate_obj(), ', cur_solution = ' + str(self.solution), 'delta = ', candidate[index].delta, 'swap', candidate[index].i, candidate[index].j)

    def tabusearch(self, maxIter, tblen):
        self.generateInitialSolution()
        tabu = [[-1 for i in range(self.nodeCount)] for i in range(self.nodeCount)]
        for it in tqdm(range(maxIter)):
            it += 1
            candidate = []
            swap_list = self.getNeighborhood(-1)
            best_delta = 0
            for i, j in swap_list:
                if (tabu[i][j] <= it):
                    delta = self.getSwapDelta(i, j)
                    if delta < best_delta:
                        best_delta = delta
                        candidate = []
                        candidate.append(Swap(i, j, delta))
                    elif delta == best_delta and len(candidate) > 0:
                        candidate.append(Swap(i, j, delta))
                    if len(candidate) > 100: break
            if len(candidate) == 0:
                if self._print: print('Reach local optimum')
                break
            index = random.randint(0, len(candidate) - 1)
            self.swapValuePropagate(candidate[index])
            tabu[candidate[index].i][candidate[index].j] = it + tblen
            if self._print: print('Step ' + str(it) + ': current obj = ' + str(self.obj) + ', cur_solution = ' + str(self.solution))

    def lnsearch(self, maxIter, neighborhood_size):
        for it in tqdm(range(maxIter)):
            swap_lists = self.getNeighborhood(neighborhood_size, 10000)
            best_delta = 0
            candidate = []
            for swap_list in swap_lists:
                delta, new_solution = self.getMultiSwapDelta(swap_list)
                if delta < best_delta:
                    candidate = []
                    candidate.append(Multiswap(delta, new_solution))
                elif delta < 0 and delta == best_delta:
                    candidate.append(Multiswap(delta, new_solution))
            if len(candidate) == 0:
                if self._print: print('Reach local optimum')
                break
            index = random.randint(0, len(candidate) - 1)
            self.swapMultiValuePropagate(candidate[index])
            if self._print: print('Step ' + str(it) + ': current obj = ' + str(self.obj) +  ', True obj = ', self.calculate_obj(), ', cur_solution = ' + str(self.solution), 'delta = ', candidate[index].delta)

    def printSolution(self):
        output_data = '%.2f' % self.obj + ' ' + str(0) + '\n'
        output_data += ' '.join(map(str, self.solution))
        print(output_data)
        print(self.calculate_obj())

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

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

# def calculate_obj(solution, points, nodeCount):
#     return sum([length(points[solution[i]], points[solution[i+1]]) for i in range(nodeCount - 1)]) + length(points[solution[nodeCount-1]], points[solution[0]])

# def generateInitialSolution(nodeCount, points):
#     L = [i for i in range(nodeCount)]
#     obj = 0
#     inititalSolution = []
#     for i in range(nodeCount):
#         index = random.randint(0, len(L) - 1)
#         inititalSolution.append(L[index])
#         if (i > 0):
#             obj += length(points[inititalSolution[i]], points[inititalSolution[i-1]])
#         L.pop(index)
#     obj += length(points[inititalSolution[nodeCount-1]], points[inititalSolution[0]])
#     if _print: print('Initial solution', inititalSolution, 'current obj = ', obj)
#     return inititalSolution, obj

# def getLength(i, j, cur_solution, points, nodeCount, i0, j0):
#     if i == nodeCount:
#         i = 0
#     if j == nodeCount:
#         j = 0
#     if i == -1:
#         i = nodeCount - 1
#     if j == -1:
#         j = nodeCount - 1
#     return length(points[cur_solution[i]], points[cur_solution[j]])

# def getSwapDelta(i, j, cur_solution, points, nodeCount):
#     delta = 0.0
#     delta += \
#         - getLength(i, i+1, cur_solution, points, nodeCount, i, j) \
#         - getLength(j, j+1, cur_solution, points, nodeCount, i, j) \
#         + getLength(i, j, cur_solution, points, nodeCount, i, j) \
#         + getLength(i+1, j+1, cur_solution, points, nodeCount, i, j)
#     return delta

# def getMultiSwapDelta(cur_solution, points, nodeCount, swapList, cur_obj):
#     new_solution = cur_solution.copy()
#     delta = 0
#     obj = cur_obj
#     for i, j in swapList:
#         delta_temp = getSwapDelta(i, j, new_solution, points, nodeCount)
#         delta += delta_temp
#         new_solution, obj = swapValuePropagate(i, j, new_solution, points, obj, nodeCount, delta_temp)
#     return delta, new_solution

# def swapValuePropagate(i, j, cur_solution, points, cur_obj, nodeCount, delta):
#     obj = cur_obj + delta
#     new_solution = cur_solution.copy()
#     if i < j:
#         new_solution = new_solution[:i+1] + new_solution[i+1:j+1][::-1] + new_solution[j+1:]
#     else:
#         new_solution = new_solution[:j+1] + new_solution[j+1:i+1][::-1] + new_solution[i+1:]
#     return new_solution, obj

# def swapMultiValuePropagate(delta, cur_obj, new_solution):
#     new_obj = cur_obj + delta
#     return new_solution, new_obj

# def getNeighborhood(nodeCount, k, list_size=1):
#     # randomly get k neiborhood from cur_solution
#     neighborhoods = []
#     if k == -1:
#         neighborhood = []
#         # get all pairs of node
#         for i in range(nodeCount-1):
#             for j in range(i+1, nodeCount-1):
#                     neighborhood.append((i, j))
#         random.shuffle(neighborhood)
#         return neighborhood
#     for i in range(list_size):
#         neighborhood = []
#         node = [i for i in range(nodeCount)]
#         while(len(neighborhood) < k):
#             idx1 = random.randint(0, len(node) - 1)
#             n1 = node[idx1]
#             node.pop(idx1)
#             idx2 = random.randint(0, len(node) - 1)
#             n2 = node[idx2]
#             node.pop(idx2)
#             neighborhood.append((n1, n2))
#         neighborhoods.append(neighborhood)
#     return neighborhoods

# def hillclimbingsearch(maxIter, nodeCount, points):
#     obj = 0
#     cur_solution, obj = generateInitialSolution(nodeCount, points)
#     for it in tqdm(range(maxIter)):
#         it += 1
#         candidate = []
#         swap_list = getNeighborhood(nodeCount, -1)
#         best_delta = 0
#         for i, j in swap_list:
#             delta = getSwapDelta(i, j, cur_solution, points, nodeCount)
#             if delta < best_delta:
#                 best_delta = delta
#                 candidate = []
#                 candidate.append(Swap(i, j, delta))
#             elif delta < 0 and delta == best_delta:
#                 candidate.append(Swap(i, j, delta))
#         if len(candidate) == 0:
#             if _print: print('Reach local optimum')
#             break
#         index = random.randint(0, len(candidate) - 1)
#         cur_solution, obj = swapValuePropagate(candidate[index].i, candidate[index].j, cur_solution, points, obj, nodeCount, candidate[index].delta)
#         if _print: print('Step ' + str(it) + ': current obj = ' + str(obj) +  ', True obj = ', calculate_obj(cur_solution, points, nodeCount), ', cur_solution = ' + str(cur_solution), 'delta = ', candidate[index].delta, 'swap', candidate[index].i, candidate[index].j)
#     return cur_solution, obj

# def tabusearch(maxIter, nodeCount, points, tblen):
#     global _print
#     obj = 0
#     cur_solution, obj = generateInitialSolution(nodeCount, points)
#     tabu = [[-1 for i in range(nodeCount)] for i in range(nodeCount)]
#     for it in tqdm(range(maxIter)):
#         it += 1
#         candidate = []
#         swap_list = getNeighborhood(nodeCount, -1)
#         best_delta = 0
#         for i, j in swap_list:
#             if (tabu[i][j] <= it):
#                 delta = getSwapDelta(i, j, cur_solution, points, nodeCount)
#                 if delta < best_delta:
#                     best_delta = delta
#                     candidate = []
#                     candidate.append(Swap(i, j, delta))
#                 elif delta == best_delta and len(candidate) > 0:
#                     candidate.append(Swap(i, j, delta))
#                 if len(candidate) > 100: break
#         if len(candidate) == 0:
#             if _print: print('Reach local optimum')
#             break
#         index = random.randint(0, len(candidate) - 1)
#         cur_solution, obj = swapValuePropagate(candidate[index].i, candidate[index].j, cur_solution, points, obj, nodeCount, candidate[index].delta)
#         tabu[candidate[index].i][candidate[index].j] = it + tblen
#         if _print: print('Step ' + str(it) + ': current obj = ' + str(obj) + ', cur_solution = ' + str(cur_solution))
#     return cur_solution, obj

# def lnsearch(maxIter, nodeCount, neighborhood_size):
#     global _print
#     obj = 0
#     cur_solution, obj = generateInitialSolution(nodeCount, points)
#     for it in tqdm(range(maxIter)):
#         swap_lists = getNeighborhood(nodeCount, 10, list_size = 10)
#         best_delta = 0
#         candidate = []
#         for swap_list in swap_lists:
#             delta, new_solution = getMultiSwapDelta(cur_solution, points, nodeCount, swap_list, obj)
#             if delta < best_delta:
#                 candidate = []
#                 candidate.append(Multiswap(delta, new_solution))
#             elif delta < 0 and delta == best_delta:
#                 candidate.append(Multiswap(delta, new_solution))
#         if len(candidate) == 0:
#             if _print: print('Reach local optimum')
#             break
#         index = random.randint(0, len(candidate) - 1)
#         cur_solution, obj = swapMultiValuePropagate(candidate[index].delta, obj, candidate[index].solution)
#         if _print: print('Step ' + str(it) + ': current obj = ' + str(obj) +  ', True obj = ', calculate_obj(cur_solution, points, nodeCount), ', cur_solution = ' + str(cur_solution), 'delta = ', candidate[index].delta)
#     return cur_solution, obj

def search1(s):
    print('HILL CLIMBING:')
    s.hillclimbingsearch(1000)
    s.printSolution()

def search2(s):
    print('TABU:')
    s.tabusearch(1000, tblen=5)
    s.printSolution()

def search3(s):
    print('LNS:')
    s.generateInitialSolution()
    s.lnsearch(1000, 20)
    s.printSolution()

nodeCount, points = readData("data/tsp_280_1")
s = Tsp(nodeCount, points)
search3(s)