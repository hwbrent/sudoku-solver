import sys
import os
import random
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

sys.path.append(os.getcwd())
sys.path.append(os.getcwd() + "/src")

from src.algorithms.algorithm import Algorithm
from src.board import Board

class StochasticSearch(Algorithm):
    '''
    https://en.wikipedia.org/wiki/Sudoku_solving_algorithms#Stochastic_search_/_optimization_methods

    Sudoku can be solved using stochastic (random-based) algorithms. An example of this method is to:
    - Randomly assign numbers to the blank cells in the grid.
    - Calculate the number of errors.
    - "Shuffle" the inserted numbers until the number of mistakes is reduced to zero.

    A solution to the puzzle is then found.

    Approaches for shuffling the numbers include:
    - simulated annealing
    - genetic algorithm
    - tabu search.

    Stochastic-based algorithms are known to be fast, though perhaps not as fast as deductive techniques.
    Unlike the latter however, optimisation algorithms do not necessarily require problems to be
    logic-solvable, giving them the potential to solve a wider range of problems.
    Algorithms designed for graph colouring are also known to perform well with Sudokus. It is also
    possible to express a Sudoku as an integer linear programming problem. Such approaches get close to a
    solution quickly, and can then use branching towards the end. The simplex algorithm is able to
    solve proper Sudokus, indicating if the Sudoku is not valid (no solution). If there is more than one
    solution (non-proper Sudokus) the simplex algorithm will generally yield a solution with fractional
    amounts of more than one digit in some squares. However, for proper Sudokus, linear programming
    presolve techniques alone will deduce the solution without any need for simplex iterations. The
    logical rules used by presolve techniques for the reduction of LP problems include the set of logical
    rules used by humans to solve Sudokus.
    '''
    
    def __init__(self, board):
        super().__init__(board)

        # Keys are tuples representing cell coordinates.
        # Corresponding values are the values placed in that cell

    def randomly_assign(self) -> 'None':
        for i, row in enumerate(self.board.spaces):
            for j, value in enumerate(row):
                if value == 0:
                    continue
                cell = (i,j)
                random_value = random.randint(1,9)
                self.board[cell] = random_value
    
    def calculate_errors(self) -> 'list[tuple[int,int]]':
        ''' Returns a `list` of cells whose values are invalid. '''
        errors = []
        for i, row in enumerate(self.board.spaces):
            for j, value in enumerate(row):
                cell = (i,j)
                if cell in self.board.clues:
                    continue
                if not self.board.is_legal_in_space(value,*cell):
                    errors.append(cell)
        return errors
    
    def shuffle(self, errors: 'list[tuple[int,int]]'):
        ''' Receives a `list` of erroneously-valued cells from `calculate_errors` and shuffles the values in those cells. '''
        pass

    def solve(self):
        pp.pprint(self.board.is_legal_in_space)
        pass

if __name__ == "__main__":
    algo = StochasticSearch([
        [0,0,0,0,0,5,0,0,3],
        [0,0,3,0,0,0,2,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,1,0,0,4,0,0,0,0],
        [0,0,0,0,5,0,0,1,2],
        [0,0,0,0,8,0,4,0,0],
        [0,0,5,0,0,0,0,0,0],
        [0,4,0,2,0,0,6,0,0],
        [7,0,6,0,0,0,0,0,0]
    ])
    algo.solve()
