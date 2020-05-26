# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 14:50:37 2020

@author: quang
"""

from ortools.sat.python import cp_model
model = cp_model.CpModel()
n = 5
_range = range(n)
var = [model.NewIntVar(0, n-1, str(i)) for i in range(n)]
for i in range(n):
    eq = []
    for j in range(n):
        e = var[j]
        tmp = model.NewBoolVar('eq_%i_%i' %(i, j))
        model.Add(e == i).OnlyEnforceIf(tmp)
        model.Add(e != i).OnlyEnforceIf(tmp.Not())
        eq.append(tmp)
    model.Add(var[i] == sum(eq))
solver = cp_model.CpSolver()
status = solver.Solve(model)
if status == cp_model.FEASIBLE:
    for i in range(n):
        print(solver.Value(var[i]), end=' ')