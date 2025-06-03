import multiprocessing
from pysat.solvers import Minisat22, Solver
from pysat.card import CardEnc, EncType
import math


class Hypergraph_Upgraded:
    def __init__(self, filename):
        self.num_edges = 0
        self.num_vertices = 0
        self.vertices = set()
        self.edges = []
        self.cnf_clauses = []  # Store precomputed CNF
        self.vertex_list = []
        self.read_hypergraph(filename)
        self._prepare_cnf()

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

    def _prepare_cnf(self):
        self.cnf_clauses = [list(edge) for edge in self.edges]
        self.vertex_list = sorted(self.vertices)

    def _solve_bound(self, bound, timeout, return_dict):
        solver = Solver(name='cadical195')
        for clause in self.cnf_clauses:
            solver.add_clause(clause)

        card = CardEnc.atmost(lits=self.vertex_list, bound=bound, encoding=EncType.seqcounter)
        for clause in card.clauses:
            solver.add_clause(clause)

        if solver.solve():
            model = solver.get_model()
            solution = {v for v in self.vertex_list if v in model}
            return_dict[bound] = solution
        solver.delete()

    def solve_hitting_set(self, initial_timeout=60.0, max_timeout=300.0):
        low, high = 1, min(len(self.vertex_list), len(self.edges))
        best_solution = None
        current_timeout = initial_timeout
        attempts = 0

        while low <= high:
            mid = (low + high) // 2
            print(f"Trying hitting set size ≤ {mid} with timeout {current_timeout:.1f}s...")

            manager = multiprocessing.Manager()
            return_dict = manager.dict()

            process = multiprocessing.Process(
                target=self._solve_bound,
                args=(mid, current_timeout, return_dict)
            )
            process.start()
            process.join(current_timeout)

            if process.is_alive():
                print("⏱️ Timeout. Increasing timeout and lower bound.")
                process.terminate()
                process.join()
                low = mid + 1

                # ▶️ Crește atât growth rate-ul, cât și timeout-ul
                attempts += 1
                growth_rate = min(1.2 + 0.1 * attempts, 1.6)
                current_timeout = min(initial_timeout * (growth_rate ** attempts), max_timeout)
                continue

            solution = return_dict.get(mid, None)
            if solution:
                best_solution = solution
                print(f"✔️ Found solution with {len(solution)} vertices: {solution}")
                high = mid - 1
            else:
                print("❌ No solution found. Trying larger bound...")
                low = mid + 1

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