from hypergraph import Hypergraph
from solver import HittingSetSolver

if __name__ == "__main__":
    hypergraph = Hypergraph("test.hgr")
    solver = HittingSetSolver(hypergraph)
    hitting_set = solver.solve()

    if hitting_set:
        print(f"Found hitting set: {hitting_set}")
    else:
        print("No hitting set found")