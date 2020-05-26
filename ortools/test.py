# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 15:43:52 2020

@author: quang
"""

from ortools.sat.python import cp_model
model = cp_model.CpModel()
tomato = model.NewIntVar(0, 100, 'tomato')
lettuce = model.NewIntVar(0, 100, 'lettuce')
spinack = model.NewIntVar(0, 100, 'spinack')
carrot = model.NewIntVar(0, 100, 'carrot')
oil = model.NewIntVar(0, 100, 'oil')
energy = model.NewIntVar(0, 1000, 'energy')
model.Add(0.85 * tomato + 1.62 * lettuce + 12.78 * spinack + 8.39 * carrot  >= 15) # at least 15g protein
model.Add(0.33 * tomato + 0.2 * lettuce + 1.58 * spinack + 1.39 * carrot >= 2) # at least 2g fat
model.Add(0.33 * tomato + 0.2 * lettuce + 1.58 * spinack + 1.39 * carrot <= 6) # at most 6g fat
model.Add(9 * tomato + 8 * lettuce + 7 * spinack + 508.2 * carrot  <= 100) # at most 100mg sodium
model.Add(energy == 21 * tomato + 16 * lettuce + 371 * spinack + 346 * carrot + 884 * oil)
solver = cp_model.CpSolver()
solver.Solve(model)
if cp_model.FEASIBLE:
    print('solution found')