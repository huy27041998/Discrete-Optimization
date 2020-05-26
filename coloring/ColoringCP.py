from ortools.sat.python import cp_model
import time
import math
class coloringCP:
    def __init__(self, edges, edge_count, node_count):
        super().__init__()
        self.edges = edges
        self.edge_count = edge_count
        self.node_count = node_count
    def stateModel(self):
        self.model = cp_model.CpModel()
        self.min_color = int(2 * math.sqrt(self.edge_count)) + 1
        # self.min_color = self.node_count
        self.x = [self.model.NewIntVar(0, self.min_color, 'edge ' + str(i)) for i in range(self.node_count)]
        for edge in self.edges:
            self.model.Add(self.x[edge[0]] != self.x[edge[1]])
            self.model.Add(self.x[edge[1]] != self.x[edge[0]])
    def solve(self):
        self.stateModel()
        start = time.time()
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 800
        solution = []
        while(1):
            for i in range(self.node_count):
                self.model.Add(self.x[i] <= self.min_color)
            if (solver.Solve(self.model) == cp_model.FEASIBLE):
                cur_solution = [solver.Value(self.x[i]) for i in range(self.node_count)]
                cur_color_num = max(cur_solution)
                if (cur_color_num < self.min_color):
                    self.min_color = cur_color_num
                    solution = cur_solution
            else: 
                break
            if time.time() - start > 600:
                break
        return self.min_color, solution

