#!/usr/bin/python
# -*- coding: utf-8 -*-


from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp
from collections import namedtuple
import math

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def MIP_solver(facility_count, customer_count, facilities, customers):
    solver = pywraplp.Solver("solve_mip", pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    x = [[solver.IntVar(0,1,'[%i][%i]' %(i, j)) for j in range(customer_count)]for i in range(facility_count)]
    y = [solver.IntVar(0,1, "[%i]" %(i)) for i  in range(facility_count)]
    # infinity = solver.infinity()
    # Calculate length from facility to customer
    d = [[0 for j in range(customer_count)]for i in range(facility_count)]
    for i in range(facility_count):
        for j in range(customer_count):
            d[i][j] = length(facilities[i].location, customers[j].location)
    # add constraint 1
    constraint1 = [solver.Constraint(1,1) for j in range(customer_count)]
    for j in range(customer_count):
        for i in range(facility_count):
            constraint1[j].SetCoefficient(x[i][j], 1)
    # add constraint 2
    constraint2 = [solver.Constraint(0, facilities[i].capacity) for i in range(facility_count)]
    for i in range(facility_count):
        for j in range(customer_count):
            constraint2[i].SetCoefficient(x[i][j], customers[j].demand)
    # add constraint 3
    constraint3 = [[solver.Constraint(0,1) for j in range(customer_count)] for i in range(facility_count)]
    for i in range(facility_count):
        for j in range(customer_count):
            constraint3[i][j].SetCoefficient(y[i], 1)       
            constraint3[i][j].SetCoefficient(x[i][j], -1)
    # add objective
    objt = solver.Objective()
    for i in range(facility_count):
        objt.SetCoefficient(y[i], facilities[i].setup_cost)
        for j in range(customer_count):
            objt.SetCoefficient(x[i][j], d[i][j])
    objt.SetMinimization()
    # solver.Minimize(sum(y[i]*facilities[i].setup_cost + sum(x[i][j]*d[i][j] for j in range(customer_count)) for i in range(facility_count)))
    # run MIP and return solution if have optimal solution
    status = solver.Solve()
    solution = []
    obj = 0
    if status == pywraplp.Solver.OPTIMAL:
        obj = int(solver.Objective().Value())
        for j in range(customer_count):
            for i in range(facility_count):
                if(x[i][j].solution_value() > 0):
                    solution.append(i)
                    break
    else :
        print("no optimal solution!")
        return
    return obj, solution 

def CP_solver(facility_count, customer_count, facilities, customers):
    model = cp_model.CpModel()
    # x = [[model.NewIntVar(0,1, "x[%i][%i]" %(i, j)) for j in range(customer_count)] for i in range(facility_count)]
    # y = [model.NewIntVar(0,1, str(i)) for i in range(facility_count)]
    x = [model.NewIntVar(0,facility_count-1, "x[%i]" %(i)) for i in range(customer_count)]
    y = [model.NewBoolVar("y[%i]" %(i)) for i in range(facility_count)]
    for i in range(facility_count):
        for j in range(customer_count):
            model.Add(x[j] == i)

    for j in range(customer_count):
        model.Add(sum([x_[j] for x_ in x]) == 1)
    z = [[model.NewIntVar(0,1<<30, "z[%i][%i]" %(i, j)) for j in range(customer_count)] for i in range(facility_count)]
    for i in range(facility_count):
        for j in range(customer_count):
            model.Add(z[i][j] == x[i][j]*customers[j].demand)
            model.Add(y[i] >= x[i][j])
    for i in range(facility_count):
        model.Add(sum(z[i]) <= facilities[i].capacity)
    t = [model.NewIntVar(0,1<<30,"t[%i]" %(i) ) for i in range(facility_count)]
    u = [[model.NewIntVar(0,1<<30, "z[%i][%i]" %(i, j)) for j in range(customer_count)] for i in range(facility_count)]
    # Calculate length from facility to customer
    d = [[0 for j in range(customer_count)]for i in range(facility_count)]
    for i in range(facility_count):
        for j in range(customer_count):
            d[i][j] = length(facilities[i].location, customers[j].location)
    for i in range(facility_count):
        model.Add(t[i] == y[i]*int(facilities[i].setup_cost))
        for j in range(customer_count):
            model.Add(u[i][j] == x[i][j]*int(d[i][j]))
    solution = []
    obj = 1<<30
    while(1):
        model.Add(sum(t)+ sum(sum(u,[])) < obj)
    # model.Minimize(sum(t)+ sum(sum(u,[])))
    # model.Minimize(sum([y[i]*facilities[i].setup_cost for i in range(facility_count)]) + sum([x[i][j]*d[i][j] for i in range(facility_count) for j in range(customer_count)]))
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 5*60
        status = solver.Solve(model)
        if(status == cp_model.FEASIBLE):
            solution = []
            obj = 0
            for i in range(facility_count):
                obj += solver.Value(t[i])
                for j in range(customer_count):
                    obj += solver.Value(u[i][j])
            for j in range(customer_count):
                for i in range(facility_count):
                    if(solver.Value(x[i][j]) > 0):
                        solution.append(i)
                        break
        else :
            print("no optimal solution!")
            break
    return obj, solution

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])
    
    facilities = []
    for i in range(1, facility_count+1):
        parts = lines[i].split()
        facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

    customers = []
    for i in range(facility_count+1, facility_count+1+customer_count):
        parts = lines[i].split()
        customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    obj, solution = MIP_solver(facility_count, customer_count,facilities, customers)
    # obj, solution = CP_solver(facility_count, customer_count,facilities, customers)
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
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)')

