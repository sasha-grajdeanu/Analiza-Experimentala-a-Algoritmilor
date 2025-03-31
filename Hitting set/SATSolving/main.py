from hypergraph import Hypergraph

if __name__ == "__main__":
    hg = Hypergraph("bremen_subgraph_100.hgr")
    optimal_hitting_set = hg.solve_hitting_set()
    print("Optimal Hitting Set:", optimal_hitting_set)

    # Verify the solution
    is_valid = hg.verify_solution(optimal_hitting_set)
    print("Is the solution valid?", is_valid)