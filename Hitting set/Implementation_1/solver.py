from pysat.solvers import Minisat22
from pysat.formula import CNF

class HittingSetSolver:
    def __init__(self, hypergraph):
        self.hypergraph = hypergraph
        self.num_vertices = len(hypergraph.vertices)

    def solve(self):
        # Create a CNF formula for the SAT solver
        formula = CNF()

        # Add clauses for each edge in the hypergraph
        for edge in self.hypergraph.edges:
            clause = [v for v in edge]  # Each edge corresponds to a disjunction of its vertices
            formula.append(clause)

        # Use a SAT solver to find a satisfying assignment
        solver = Minisat22()
        solver.append_formula(formula)

        # Minimize the number of selected vertices
        best_hitting_set = None
        for num_selected_vertices in range(1, self.num_vertices + 1):
            solver = Minisat22()
            solver.append_formula(formula)

            # Add cardinality constraint (optimize for the smallest set)
            # This constraint checks that exactly `num_selected_vertices` are selected
            solver.add_clause([v for v in range(1, self.num_vertices + 1) if v != num_selected_vertices])

            if solver.solve():
                model = solver.get_model()
                hitting_set = {abs(v) for v in model if v > 0}
                best_hitting_set = hitting_set
                break

        return best_hitting_set