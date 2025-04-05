import multiprocessing
from pysat.solvers import Minisat22
from pysat.card import CardEnc, EncType


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
                if line.startswith('c'):
                    continue
                if line.startswith('p'):
                    _, _, v, e = line.split()
                    self.num_vertices, self.num_edges = int(v), int(e)
                else:
                    edge = set(map(int, line.split()))
                    self.edges.append(edge)
                    self.vertices.update(edge)

    def to_cnf(self):
        return [list(edge) for edge in self.edges]

    def _solve_with_timeout(self, solver, solution):
        if solver.solve():
            model = solver.get_model()
            solution.append({abs(v) for v in model if v > 0 and v in self.vertices})

    def solve_hitting_set(self, timeout=300.0):
        cnf = self.to_cnf()
        left, right = 1, min(len(self.vertices), len(self.edges))
        best_solution = None

        while left <= right:
            mid = (left + right) // 2
            print(f"Checking hitting set size ≤ {mid}...")

            solver = Minisat22()
            for clause in cnf:
                solver.add_clause(clause)

            at_most_k = CardEnc.atmost(lits=list(self.vertices), bound=mid, encoding=EncType.seqcounter)
            for clause in at_most_k.clauses:
                solver.add_clause(clause)

            solution = multiprocessing.Manager().list()
            process = multiprocessing.Process(target=self._solve_with_timeout, args=(solver, solution))
            process.start()
            process.join(timeout)

            if process.is_alive():
                print(f"Timeout exceeded ({timeout}s). Increasing hitting set size...")
                process.terminate()
                process.join()
                solver.delete()
                left = mid + 1
                continue

            if solution:
                best_solution = solution[0]
                print(f"Found solution with {len(best_solution)} elements: {best_solution}")
                right = mid - 1
            else:
                left = mid + 1

            solver.delete()

        return best_solution

    def solve_greedy(self):
        remaining_sets = [set(edge) for edge in self.edges]
        hitting_set = set()

        while remaining_sets:
            element_counts = {}
            for s in remaining_sets:
                for element in s:
                    element_counts[element] = element_counts.get(element, 0) + 1

            if not element_counts:
                break

            best_element = max(element_counts, key=element_counts.get)
            hitting_set.add(best_element)

            remaining_sets = [s for s in remaining_sets if best_element not in s]

        return hitting_set


    def verify_solution(self, hitting_set):
        for edge in self.edges:
            if not any(vertex in hitting_set for vertex in edge):
                return False
        return True
