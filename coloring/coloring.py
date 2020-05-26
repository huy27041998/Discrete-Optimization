# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 17:38:41 2020

@author: quang
"""

from ortools.sat.python import cp_model
model = cp_model.CpModel()
class FindBestSolution:
    def __init__(self, varibles, solver):
        super().__init__()
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.best_value = float('inf')
        self.varibles = varibles
        self.solver = solver
    def on_solution_callback(self):
        print('called')
#        obj = self.ObjectiveValue()
#        if (self.best_value > obj):
#            self.best_value = obj
#            print(f'New Best Value: {self.best_value}') 
    def ObjectValue(self):
        res = 0
        for varible in self.varibles:
            res += self.solver.Value(varible)
        return res
def solution_callback():
    print('called')
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
    model = cp_model.CpModel()        
    print('node %d, edge %d' %(node_count, edge_count))
    x = [model.NewIntVar(0, node_count, str(i)) for i in range(node_count)] #value of x[i]: color of node[i]
    y = [[model.NewBoolVar('eq_i_j' %(i, j)) for i in range(node_count)] for j in range(node_count)]
    z = [[model.NewBoolVar('eq_i_j' %(x[i], x[j])) for i in range(node_count)] for j in range(node_count)]
    violations = model.Add(sum(y[i])).OnlyEnforceIf(y and z)
    for edge in edges:
        model.Add(x[edge[0]] != x[edge[1]])
    for i in node_count
        model.Add(x[edge[0]] != x[edge[1]]).OnlyEnforceIf(y[i][j])
        model.Add(x[edge[0]] != x[edge[1]]).OnlyEnforceIf(y[i][j].Not())
    solver = cp_model.CpSolver()
    solver.parameters.log_search_progress = True
    best = FindBestSolution(x, solver)
    # solver.SolveWithSolutionCallback(model, solution_callback)
    solver.Solve(model)
    print('violations = %d' %(solver.Value(violations)))
    solution = [solver.Value(x[i]) for i in range(node_count)]
    output_data = str() + ' ' + str(0) + '\n'
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')