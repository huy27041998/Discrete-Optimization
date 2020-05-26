from ortools.sat.python import cp_model
import time
model = cp_model.CpModel()
board_size = 300
queens = [model.NewIntVar(0, board_size - 1, 'x%i' % i) for i in range(board_size)]
    
 # The following sets the constraint that all queens are in different rows.
model.AddAllDifferent(queens)
model.Add(queens[0] == 0)
  # Note: all queens must be in different columns because the indices of queens are all different.
diag1 = []
diag2 = []
for j in range(board_size):
  # Create variable array for queens(j) + j.
  q1 = model.NewIntVar(0, 2 * board_size, 'diag1_%i' % j)
  diag1.append(q1)
  model.Add(q1 == queens[j] + j)
  # Create variable array for queens(j) - j.
  q2 = model.NewIntVar(-board_size, board_size, 'diag2_%i' % j)
  diag2.append(q2)
  model.Add(q2 == queens[j] - j)
start = time.time()
model.AddAllDifferent(diag1)
model.AddAllDifferent(diag2)
model.Add(queens[0] < int(board_size/2))
model.Add(queens[-1] >= int(board_size/2))
solver = cp_model.CpSolver()
solver.Solve(model)
if cp_model.FEASIBLE:
    print([solver.Value(queens[i]) for i in range(board_size)])
elif cp_model.INFEASIBLE:
    print('not found')
print(time.time() - start)