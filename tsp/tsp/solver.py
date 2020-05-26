#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])
Swap = namedtuple("Swapmove", ['i', 'j', 'delta'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def calculate_obj(solution, points, nodeCount):
    return sum([length(points[solution[i]], points[solution[i+1]]) for i in range(nodeCount - 1)]) + length(points[solution[nodeCount-1]], points[solution[0]])

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

def generateInitialSolution(nodeCount, points):
    L = [i for i in range(nodeCount)]
    obj = 0
    inititalSolution = []
    for i in range(nodeCount):
        index = random.randint(0, len(L) - 1)
        inititalSolution.append(L[index])
        if (i > 0):
            obj += length(points[inititalSolution[i]], points[inititalSolution[i-1]])
        L.pop(index)
    obj += length(points[inititalSolution[nodeCount-1]], points[inititalSolution[0]])
    return inititalSolution, obj

def getLength(i, j, cur_solution, points, nodeCount, i0, j0):
    if i == nodeCount:
        i = 0
    if j == nodeCount:
        j = 0
    if i < 0 or j < 0 or i > nodeCount - 1 or j > nodeCount -1 or i == j or (i == i0 and j == j0) or (i == j0 and j == i0): 
        return 0
    else:
        return length(points[cur_solution[i]], points[cur_solution[j]])

def getSwapDelta(i, j, cur_solution, points, nodeCount):
    delta = 0
    delta += \
        - getLength(i, i-1, cur_solution, points, nodeCount, i, j) - getLength(i, i+1, cur_solution, points, nodeCount, i, j) \
        - getLength(j, j-1, cur_solution, points, nodeCount, i, j) - getLength(j, j+1, cur_solution, points, nodeCount, i, j) \
        + getLength(j, i-1, cur_solution, points, nodeCount, i, j) + getLength(j, i+1, cur_solution, points, nodeCount, i, j) \
        + getLength(i, j+1, cur_solution, points, nodeCount, i, j) + getLength(i, j-1, cur_solution, points, nodeCount, i, j)
    return delta

def getMultiSwapDelta(cur_solution, points, nodeCount, swapList, cur_obj):
    new_solution = cur_solution
    delta = 0
    for i, j in swapList:
        delta_temp = getSwapDelta(i, j, new_solution, points, nodeCount)
        delta += delta_temp
        new_solution = swapValuePropagate(i, j, calculate_obj, points, cur_obj, nodeCount, delta_temp)
    return new_solution, delta

def swapValuePropagate(i, j, cur_solution, points, cur_obj, nodeCount, delta):
    obj = cur_obj + delta
    cur_solution[i], cur_solution[j] = cur_solution[j], cur_solution[i]
    return cur_solution, obj

def getNeighborhood(nodeCount, k):
    # randomly get k neiborhood from cur_solution
    node = [i for i in range(nodeCount)]
    neiborhood = []
    if k == -1:
        # get all pairs of node
        for i in range(nodeCount):
            for j in range(i+1, nodeCount):
                if i != j:
                    neiborhood.append((i, j))
        return neiborhood
    while(len(neiborhood) < k):
        n1 = random.randint(0, len(node) - 1)
        node.pop(n1)
        n2 = random.randint(0, len(node) - 1)
        node.pop(n2)
        neiborhood.append((n1, n2))
    return neiborhood

def search(maxIter, nodeCount, points, neiborhood_size):
    it = 0
    obj = 0
    cur_solution, obj = generateInitialSolution(nodeCount, points)
    while(it < maxIter):
        it += 1
        candidate = []
        swap_list = getNeighborhood(nodeCount, neiborhood_size)
        for i, j in swap_list:
            delta = getSwapDelta(i, j, cur_solution, points, nodeCount)
            if delta < 0:
                candidate = []
                candidate.append(Swap(i, j, delta))
            elif delta == 0 and len(candidate) > 0 and len(candidate) < 1000:
                candidate.append(Swap(i, j, delta))
        if len(candidate) == 0:
            # print('Reach local optimum')
            break
        index = random.randint(0, len(candidate) - 1)
        cur_solution, obj = swapValuePropagate(candidate[index].i, candidate[index].j, cur_solution, points, obj, nodeCount, candidate[index].delta)
        # print('Step ' + str(it) + ': current obj = ' + str(obj) + ', cur_solution = ' + str(cur_solution))
    return cur_solution, obj

def tabusearch(maxIter, nodeCount, points, tblen):
    it = 0
    obj = 0
    cur_solution, obj = generateInitialSolution(nodeCount, points)
    tabu = [[-1 for i in range(nodeCount)] for i in range(nodeCount)]
    while(it < maxIter):
        it += 1
        candidate = []
        swap_list = getNeighborhood(nodeCount, -1)
        for i, j in swap_list:
            if (tabu[i][j] <= it):
                delta = getSwapDelta(i, j, cur_solution, points, nodeCount)
                if delta < 0:
                    candidate = []
                    candidate.append(Swap(i, j, delta))
                elif delta == 0 and len(candidate) > 0:
                    candidate.append(Swap(i, j, delta))
        if len(candidate) == 0:
            # print('Reach local optimum')
            break
        index = random.randint(0, len(candidate) - 1)
        cur_solution, obj = swapValuePropagate(candidate[index].i, candidate[index].j, cur_solution, points, obj, nodeCount, candidate[index].delta)
        tabu[candidate[index].i][candidate[index].j] = it + tblen
        # print('Step ' + str(it) + ': current obj = ' + str(obj) + ', cur_solution = ' + str(cur_solution))
    return cur_solution, obj

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))
    # build a trivial solution
    # visit the nodes in the order they appear in the file
    if (nodeCount < 500):
        maxIter = 1000
        neiborhood_size = -1
    elif nodeCount < 1000:
        maxIter = 2000
        neiborhood_size = 20
    else: 
        maxIter = 1000
        neiborhood_size = 100
    solution, obj = search(maxIter, nodeCount, points, neiborhood_size)
    # prepare the solution in the specified output format
    output_data = '%.2f' % obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')

