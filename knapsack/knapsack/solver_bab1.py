#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math
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
    def branch_and_bound(capacity, value, taken):
        items.sort(key=lambda x: -x.value / x.weight)
        cur_weight = 0
        cur_value = 0
        for i in range(item_count):
            taken[items[i].index], cur_value, cur_weight = compute_up_and_lower_bound(items, item_count, i, cur_value, cur_weight, capacity)
        print('final weight: ' + str(cur_weight))
        return cur_value, taken, 0
    value, taken, algo = branch_and_bound(capacity, value, taken)
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(algo) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

def compute_up_and_lower_bound(items, item_count, i, cur_value, cur_weight, w):
    if (i == item_count - 1):
        if (cur_weight + items[i].weight <= w):
            return 1, cur_value + items[i].value, cur_weight + items[i].weight
        else: 
            return 0, cur_value, cur_weight
    e1 = e2 = cur_value
    cur_weight1 = cur_weight  + items[i].weight
    e1 += items[i].value
    cur_weight2 = cur_weight
    for j in range(i+1, item_count):
        if (cur_weight1 + items[j].weight <= w):
            e1 += items[j].value
            cur_weight1 += items[j].weight
        else:
            e1 += items[j].value * (w - cur_weight1) / items[j].weight
            break
    for j in range(i+1, item_count):
        if (cur_weight2 + items[j].weight <= w):
            e2 += items[j].value
            cur_weight2 += items[j].weight
        else:
            e2 += items[j].value * (w - cur_weight2) / items[j].weight 
            break
    print('x[' + str(i) + '] = 1, estimate 1 = ' + str(e1) + '\tx[' + str(i) + '] = 0, estimate2 =  ' + str(e2))
    if (e1 > e2 and cur_weight + items[i].weight <= w):
        return 1, cur_value + items[i].value, cur_weight + items[i].weight
    else:
        return 0, cur_value, cur_weight

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

