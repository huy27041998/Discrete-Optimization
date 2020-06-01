import numpy as np
from simplex_integer import simplex_integer
from fractions import Fraction
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True, help = 'Path to image')
args = vars(ap.parse_args())
# np.set_printoptions(suppress=True, formatter={'all':lambda x: str(Fraction(x).limit_denominator())})

s = simplex_integer(args['file'], _print = False)
s.printSolution()