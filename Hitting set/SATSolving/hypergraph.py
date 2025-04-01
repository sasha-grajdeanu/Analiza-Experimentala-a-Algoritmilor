from pysat.solvers import Minisat22, Glucose4
from pysat.card import CardEnc
import time


class Hypergraph:
    def __init__(self, filename):
        self.num_edges = None
        self.num_vertices = None
        self.vertices = set()
        self.edges = []
        self.read_hypergraph(filename)

    def read_hypergraph(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("c"):
                    continue
                if line.startswith("p"):
                    _, _, v, e = line.split()
                    self.num_vertices, self.num_edges = int(v), int(e)
                else:
                    edge = set(map(int, line.split()))
                    self.edges.append(edge)
                    self.vertices.update(edge)

    def to_cnf(self):
        return [list(edge) for edge in self.edges]

    def solve_hitting_set(self, max_time_per_mid=5):
        cnf = self.to_cnf()
        left, right = 1, min(len(self.vertices), len(self.edges))  # Optimized binary search range
        best_solution = None

        while left <= right:
            mid = (left + right) // 2
            print(f"Checking hitting set size ≤ {mid}...")

            start_time = time.time()
            solver = Glucose4() if mid > 50 else Minisat22()  # Choose faster solver

            for clause in cnf:
                solver.add_clause(clause)

            encoding_type = 2 if len(self.vertices) > 100 else 1
            at_most_k = CardEnc.atmost(lits=list(self.vertices), bound=mid, encoding=encoding_type)

            for clause in at_most_k.clauses:
                solver.add_clause(clause)

            # Solve with a timeout condition
            solved = solver.solve_limited(expect_interrupt=True)  # Non-blocking solve
            elapsed = time.time() - start_time

            if elapsed > max_time_per_mid:  # If mid is taking too long, increase `mid`
                print(f"Skipping mid={mid} (too slow: {elapsed:.2f}s)")
                left = mid + 1
                solver.delete()
                continue

            if solved:
                model = solver.get_model()
                hitting_set = {abs(v) for v in model if v > 0 and v in self.vertices}
                best_solution = hitting_set
                print(f"✅ Found solution with {len(hitting_set)} elements: {hitting_set}")
                right = mid - 1
            else:
                left = mid + 1

            solver.delete()  # Free up memory

        return best_solution

    def verify_solution(self, hitting_set):
        return all(any(vertex in hitting_set for vertex in edge) for edge in self.edges)

