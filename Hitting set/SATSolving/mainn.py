import os
import time
from hypergraph import Hypergraph
from hypergraph_upgrade import Hypergraph_Upgraded

RESULTS_FILE = "results_cadical.txt"

def log_result(text):
    with open(RESULTS_FILE, "a") as f:
        f.write(text + "\n")

def main():
    open(RESULTS_FILE, "w").close()

    for filename in os.listdir("."):
        if filename.startswith("bremen_") and filename.endswith(".hgr"):
            print(f"\nProcessing {filename}...")
            log_result(f"==== {filename} ====")

            hg = Hypergraph_Upgraded(filename)

            # --- Greedy Method ---
            start = time.time()
            greedy_solution = hg.solve_greedy()
            greedy_time = time.time() - start
            is_greedy_valid = hg.verify_solution(greedy_solution)

            log_result(f"Greedy Hitting Set: {sorted(greedy_solution)}")
            log_result(f"Greedy Time: {greedy_time:.2f}s")
            log_result(f"Greedy Valid: {is_greedy_valid}")
            log_result(f"Greedy Size: {len(greedy_solution)}")

            # --- SAT Method ---
            start = time.time()
            sat_solution = hg.solve_hitting_set()
            sat_time = time.time() - start
            is_sat_valid = hg.verify_solution(sat_solution)

            log_result(f"SAT Hitting Set: {sorted(sat_solution)}")
            log_result(f"SAT Time: {sat_time:.2f}s")
            log_result(f"SAT Valid: {is_sat_valid}")
            log_result(f"SAT Size: {len(sat_solution)}")

            # --- Summary ---
            optimal = (
                "SAT"
                if len(sat_solution) < len(greedy_solution)
                else "Greedy"
            )
            log_result(f"Best Method: {optimal}")
            log_result("")

if __name__ == "__main__":
    main()
