#!/usr/bin/python
# -*- coding: utf-8 -*-
from ColoringCP import coloringCP
from subprocess import Popen, PIPE
from ortools.sat.python import cp_model
import math, time, os
def solve_python(edges, edge_count, node_count):
    model = cp_model.CpModel()
    cvar = [model.NewIntVar(0,int(math.sqrt(edge_count)),str(i)) for i in range(node_count)]
    solution =[]
    for e in edges:
        model.Add(cvar[e[0]] != cvar[e[1]])
    count_color = int(math.sqrt(edge_count))+1
    start_time = time.time()
    while(1):
        end_time = time.time()
        if(int(end_time)-int(start_time) > 60*10):
            break
        for i in range(node_count):
            model.Add(cvar[i] < count_color)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 60*10
        status = solver.Solve(model)
        if( status == cp_model.FEASIBLE):
            solution.clear()
            for i in range(node_count):
                solution.append( int(solver.Value(cvar[i])))
            count_color = max(solution) 
        else:
            break
    output_data = str(count_color+1) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    return output_data
def solve_java(input_data):
    tmp_file_name = 'tmp.data'
    tmp_file = open(tmp_file_name, 'w')
    tmp_file.write(input_data)
    tmp_file.close()

    # Runs the command: java Solver -file=tmp.data

    process = Popen(['java', '-jar', 'Test.jar', '-file=' + tmp_file_name], stdout=PIPE)
    (stdout, stderr) = process.communicate()

    # removes the temporay file
    os.remove(tmp_file_name)
    
    return stdout.decode('utf-8').strip()
def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])
    edges = []

    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
    # if node_count < 500:
    #     return solve_python(edges, edge_count, node_count)
    # else:
    return solve_java(input_data)
    return ''



import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

