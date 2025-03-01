from ortools.sat.python import cp_model

class Printers(cp_model.CpSolverSolutionCallback):
    def __init__(self, queens):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__queens = queens
        self.__solution_count = 0

    def on_solution_callback(self):
        self.__solution_count += 1
        print(f"Solution {self.__solution_count}:")

        # Get queen positions
        queen_positions = [self.Value(q) for q in self.__queens]

        # Print the board
        for row in range(len(self.__queens)):
            for col in range(len(self.__queens)):
                if queen_positions[col] == row:
                    print("Q", end=" ")
                else:
                    print("_", end=" ")
            print()
        print()

    def solution_count(self):
        return self.__solution_count

def solve_n_queens(blocked_positions):
    model = cp_model.CpModel()

    queens = [model.NewIntVar(0, 3, f"queen{i}") for i in range(4)]

    model.AddAllDifferent(queens)
    model.AddAllDifferent([queens[i] + i for i in range(4)])
    model.AddAllDifferent([queens[i] - i for i in range(4)])

    for row, col in blocked_positions:
        model.Add(queens[col] != row)

    # Solve the model
    solver = cp_model.CpSolver()
    solver_printer = Printers(queens)
    solver.parameters.enumerate_all_solutions = True
    solver.Solve(model, solver_printer)

    print(f"Total solutions found: {solver_printer.solution_count()}")

if __name__ == "__main__":
    blocked = [(0, 1), (1, 0), (2, 3), (3, 1)]
    blocked_two = []
    solve_n_queens(blocked)
