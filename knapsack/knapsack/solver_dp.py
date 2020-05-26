#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    taken = [0]*len(items)


    def dp_solve(capacity, value, taken):
        A = [[0 for i in range(item_count + 1)] for i in range(capacity + 1)]
        for i in range(capacity+1):
            for j in range(item_count + 1):
                if A[i][j] == 0 and j > 0:
                    if (items[j-1].weight <= i):
                        A[i][j] = max(A[i][j - 1], items[j - 1].value + A[i - items[j - 1].weight][j - 1])
                    else:
                        A[i][j] = A[i][j - 1]
        #traceback
        value = A[capacity][item_count]
        for i in range(item_count, 0, -1):
            if (A[capacity][i] != A[capacity][i-1]):
                taken[i-1] = 1
                capacity -= items[i-1].weight
        return value, taken, 1
    def greedy(capacity, value, taken):
        items.sort(key=lambda x: -x.value)
        cur_weight = 0
        for i in range(item_count):
            if (items[i].weight + cur_weight <= capacity):
                taken[items[i].index] = 1
                value += items[i].value
                cur_weight += items[i].weight
        return value, taken, 0
    if (item_count * capacity > (1 << 28)):
        value, taken, algo = greedy(capacity, value, taken)
    else: 
        value, taken, algo = dp_solve(capacity, value, taken)
    output_data = str(value) + ' ' + str(algo) + '\n'
    output_data += ' '.join(map(str, taken))
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

