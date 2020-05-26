from ortools.sat.python import cp_model
import time
class coloringCP:
    def __init__(self, edges, edge_count, node_count):
        super().__init__()
        self.edges = edges
        self.edge_count = edge_count
        self.node_count = node_count
    def stateModel(self):
        self.model = cp_model.CpModel()
        self.x = [self.model.NewIntVar(0, self.node_count, 'edge ' + str(i)) for i in range(self.node_count)]
        self.color_num = self.model.NewIntVar(0, self.node_count, 'color_num')
        for edge in self.edges:
            self.model.Add(self.x[edge[0]] != self.x[edge[1]])
            self.model.Add(self.x[edge[1]] != self.x[edge[0]])
            self.min_color = self.node_count
            self.model.AddMaxEquality(self.color_num, self.x)
    def solve(self):
        self.stateModel()
        start = time.time()
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 300
        while(1):
            self.model.Add(self.color_num <= self.min_color)
            if (solver.Solve(self.model) == cp_model.FEASIBLE):
                if (solver.Value(self.color_num) < self.min_color):
                    self.min_color = solver.Value(self.color_num)
            else: 
                break
            if time.time() - start > 60:
                break
        return self.min_color, [solver.Value(self.x[i]) for i in range(self.node_count)]

