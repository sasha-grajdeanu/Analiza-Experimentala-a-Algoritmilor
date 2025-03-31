from pysat.solvers import Minisat22
from pysat.card import CardEnc


class Hypergraph:
    def __init__(self, filename):
        self.num_edges = None
        self.num_vertices = None
        self.vertices = set()
        self.edges = []
        self.read_hypergraph(filename)

    def read_hypergraph(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line.startswith('c'):
                    continue 
                if line.startswith('p'):
                    parts = line.split()
                    self.num_vertices = int(parts[2])
                    self.num_edges = int(parts[3])
                else:
                    edge = set(map(int, line.split()))
                    self.edges.append(edge)
                    self.vertices.update(edge)

    def to_cnf(self):
        cnf = []
        for edge in self.edges:
            cnf.append(list(edge))
        return cnf

    def solve_hitting_set(self):
        cnf = self.to_cnf()
        solver = Minisat22()
        for clause in cnf:
            solver.add_clause(clause)

        left, right = 1, len(self.vertices)
        best_solution = None

        while left <= right:
            mid = (left + right) // 2
            solver = Minisat22()

            for clause in cnf:
                solver.add_clause(clause)

            at_most_k = CardEnc.atmost(lits=list(self.vertices), bound=mid, encoding=1)
            for clause in at_most_k.clauses:
                solver.add_clause(clause)

            if solver.solve():
                model = solver.get_model()
                hitting_set = [v for v in self.vertices if model[v - 1] > 0]
                best_solution = hitting_set
                right = mid - 1
            else:
                left = mid + 1

        return best_solution

    def verify_solution(self, hitting_set):
        for edge in self.edges:
            if not any(vertex in hitting_set for vertex in edge):
                return False
        return True