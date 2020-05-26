# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 20:58:40 2020

@author: quang
"""

from ortools.sat.python import cp_model
model = cp_model.CpModel()
country = []
color = []
n = len(country)
x = [model.NewIntervalVar(0, len(color), str(i)) for in in range(n)]
for i in range(n):
    model.Add(x[i] != x[j])
solver = cp_model.CpSolver()
status = solver.Solve(model)
if status == cp_model.FEASIBLE:
    for i in range(country):
        print(country[i] + ': ' + color[solver.Value(x[i])])