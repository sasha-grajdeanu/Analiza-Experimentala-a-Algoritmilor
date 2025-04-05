from hypergraph import Hypergraph

if __name__ == "__main__":
    hg = Hypergraph("bremen_subgraph_300.hgr")
    # optimal_hitting_set = hg.solve_hitting_set()
    optimal_hitting_set = hg.solve_greedy()
    print("Optimal Hitting Set:", optimal_hitting_set)

    is_valid = hg.verify_solution(optimal_hitting_set)
    print("Is the solution valid?", is_valid)
    print(len(optimal_hitting_set))