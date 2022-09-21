import random
from pprint import PrettyPrinter

from board import Board

pp = PrettyPrinter(indent=4)

class Backtracking:

    board1 = [[0, 0, 0, 0, 0, 5, 0, 0, 3], [0, 0, 3, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 1, 2], [0, 0, 0, 0, 8, 0, 4, 0, 0], [0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 4, 0, 2, 0, 0, 6, 0, 0], [7, 0, 6, 0, 0, 0, 0, 0, 0]]

    def __init__(self, board:'list[list[int]]|None' = None):
        '''
        `self.board` encodes the Sudoku board.

        `self.options` (will) consist of a `dict` where each key is a `tuple` representing a space, and the value is a `list` of `int`s encoding the values that the space can take at a given point in time.
        '''
        self.board = Board(board if board else Backtracking.board1)
        self.options = {}
        
        # pp.pprint(self.board)
        print(self.board.spaces)

    # ---------------

    def check_options(self, i:'int', j:'int', options:'list'):
        # if not 
        space = (i,j)
        if not space in self.options.keys():
            self.options[space] = options
        pass

    # ---------------

    def backtrack(self, i:'int', j:'int') -> 'tuple[int,int]':
        # This method is called when there are no valid options for the space with coordinates (i,j).
        # That means we need to go back to the previous (non-clue) space and try the next valid value.

        # del self.options[(i,j)]

        # Find the last space which isn't a clue.
        # Basically, iterate backwards from the current (i,j) through to the start of the board.
        prev_space = self.board.get_prev_space(i,j)
        while len(self.options[prev_space]) in [0,1]: # if the prev space
            prev_space = self.board.get_prev_space(*prev_space)
        
        print(prev_space)


    def solve(self):
        ''' Solves the current board. '''

        i = 0
        while i < len(self.board):
            j = 0
            while j < len(self.board):
                
                space_value = self.board[i][j]

                if (space_value != 0) or (not (i,j) in self.board.clues):

                    # Find the options for this particular space.
                    options = self.board.get_options(i,j)

                    if len(options) != 0:
                        # Get the first option and assign it
                        self.board[i][j] = options[0]

                        # Update self.options with the options that the current space had at the time.
                        # This is used when backtracking
                        self.options[(i,j)] = options

                    else:
                        # Backtrack here!
                        # Here, there are no valid options for the space with coordinates (i,j).
                        # That means we need to go back to the previous (non-clue) space and try the next valid value.
                        self.backtrack(i,j)
                        continue

                    print(i,j,space_value, options)

                j += 1
            i += 1

def main():
    solver = Backtracking()
    # solver.solve()
    solver.backtrack(3,3)

if __name__ == "__main__":
    main()
