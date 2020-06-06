import numpy as np
from simplex_integer1 import simplex_integer
from fractions import Fraction
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help = 'Path to image')
args = vars(ap.parse_args())
# np.set_printoptions(suppress=True, formatter={'all':lambda x: str(Fraction(x).limit_denominator())})

s = simplex_integer(args['file'], _print = False)
print('branch and bound')
if (s.solve_branch_and_bound()):
    s.printSolution()
else:
    print('Solution not found')
print('gomory cut')
if (s.solve_gomory()):
    s.printSolution()
else:
    print('Solution not found')