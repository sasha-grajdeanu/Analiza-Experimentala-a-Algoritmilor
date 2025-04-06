import multiprocessing
from pysat.solvers import Minisat22
from pysat.card import CardEnc, EncType


class Hypergraph:
    def __init__(self, filename):
        self.num_edges = 0
        self.num_vertices = 0
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

    def _solve_with_timeout(self, cnf_clauses, vertex_list, bound, return_dict):
        solver = Minisat22()
        for clause in cnf_clauses:
            solver.add_clause(clause)

        # Add cardinality constraint: at most 'bound' vertices selected
        card = CardEnc.atmost(lits=vertex_list, bound=bound, encoding=EncType.seqcounter)
        for clause in card.clauses:
            solver.add_clause(clause)

        if solver.solve():
            model = solver.get_model()
            solution = {v for v in vertex_list if v in model}
            return_dict["solution"] = solution
        solver.delete()

    def solve_hitting_set(self, timeout=300.0):
        cnf = [list(edge) for edge in self.edges]
        vertex_list = sorted(self.vertices)

        left, right = 1, min(len(vertex_list), len(self.edges))
        best_solution = None

        while left <= right:
            mid = (left + right) // 2
            print(f"Trying hitting set size ≤ {mid}...")

            manager = multiprocessing.Manager()
            return_dict = manager.dict()

            process = multiprocessing.Process(
                target=self._solve_with_timeout,
                args=(cnf, vertex_list, mid, return_dict)
            )
            process.start()
            process.join(timeout)

            if process.is_alive():
                print(f"Timeout after {timeout}s. Increasing bound...")
                process.terminate()
                process.join()
                left = mid + 1
                continue

            solution = return_dict.get("solution", None)
            if solution:
                best_solution = solution
                print(f"✔️ Found solution with {len(solution)} vertices: {solution}")
                right = mid - 1
            else:
                print("❌ No solution found. Increasing size...")
                left = mid + 1

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
