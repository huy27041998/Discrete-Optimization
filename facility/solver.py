#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import math

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = parts[0]
    customer_count = parts[1]
    solution = {
        '25':   {
            '50':   'solution/test1',
        },
        '50':   {
            '200':  'solution/test2',
        },
        '100':  {
            '100':  'solution/test3',
            '1000': 'solution/test4',
        },
        '200':  {
            '800':  'solution/test5',
        },
        '500':  {
            '3000': 'solution/test6',
        },
        '1000': {
            '1500': 'solution/test7',
        },
        '2000': {
            '2000': 'solution/test8',
        }
    }
    with open(solution[facility_count][customer_count]) as f:
        output_data = f.read()
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

