#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

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
    solution = range(0, nodeCount)
    # calculate the length of the tour
    mark = [[0 for i in range(nodeCount)] for i in range(1 << nodeCount)]
    def generateSubset(seed):
        subset = list()
        for i in range(1, nodeCount):
            if ((seed & (1 << i)) >> i) == 1:
                subset.append((seed & ~(1 << i), i))
        return subset
    def cost(_id, j):
        subsets = generateSubset(_id)
        if mark[_id][j] > 0:
            return mark[_id][j]
        if len(subsets) == 0: 
            return length(points[0], points[j])
        _min = sys.maxsize
        id_min = 0
        eliminated = 0
        for subset in subsets:
            subset_value = cost(subset[0], subset[1])
#            print('{0:b}'.format(subset[0]) + ' ' + str(subset[1]) + ' ' + str(subset_value))
            if (_min > subset_value + length(points[j], points[subset[1]])):
                _min = subset_value + length(points[j], points[subset[1]])
                id_min = subset[0]
                eliminated = subset[1]
#                temp = 
        print('{0:b}'.format(id_min) + ' ' + str(eliminated) + ' ' + str(_min))
        mark[id_min][eliminated] = _min
        return _min
    obj = cost((1 << nodeCount) - 2, 1)
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

