import sys
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

from board import Board

# ==============================

class Backtracking:

    board1 = [[0, 0, 0, 0, 0, 5, 0, 0, 3], [0, 0, 3, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 1, 0, 0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 1, 2], [0, 0, 0, 0, 8, 0, 4, 0, 0], [0, 0, 5, 0, 0, 0, 0, 0, 0], [0, 4, 0, 2, 0, 0, 6, 0, 0], [7, 0, 6, 0, 0, 0, 0, 0, 0]]

    def __init__(self, board:'list[list[int]]|None' = None, __print:'bool' = False):
        '''
        `self.board` encodes the Sudoku board.

        `self.options` (will) consist of a `dict` where each key is a `tuple` representing a space, and the value is a `list` of `int`s encoding the values that the space can take at a given point in time.
        '''
        self.board = Board(board if board else Backtracking.board1, __print)
        self.options = {}

        # Used after the board is complete. Can tell functions to print to show if
        # the board has been filled successfully.
        self.__print = __print
        
        print(self.board.spaces)

    # ---------------

    def backtrack(self, i:'int', j:'int') -> 'tuple[int,int]':
        # This method is called when there are no valid options for the space with coordinates (i,j).
        # That means we need to go back to the previous (non-clue) space and try the next valid value.

        # del self.options[(i,j)]

        if self.__print: print("(backtrack) backtracking on", (i,j))

        # Find the last space which isn't a clue.
        # Basically, iterate backwards from the current (i,j) through to the start of the board.
        prev_space = self.board.get_prev_space(i,j)
        
        prev_space_value = self.board[prev_space]

        # print("(backtrack) prev_space:", prev_space)
        # print("(backtrack) prev_space_value:", prev_space_value)
        # print("(backtrack) prev_space options:", self.options[prev_space])

        # If the space only has 1 option, that's the current value of the space, so need to backtrack further
        if len(self.options[prev_space]) <= 1:
            # print(f"(backtrack) len(self.options[{prev_space}]) = {len(self.options[prev_space])}:")

            # Reset the value of the space
            self.board[prev_space] = 0

            # Remove the entry in `self.options`
            del self.options[prev_space]

            # Recurse onto the next previous space
            return self.backtrack(*prev_space)

        else:
            if self.__print: print(f"(backtrack) prev space: {prev_space}")

            assert(not prev_space in self.board.clues)

            # Discard the first option.
            # (Because that's the value that the space previously had
            # which led to us needing to backtrack)
            # del self.options[prev_space][0]
            opts = self.options[prev_space]
            self.options[prev_space] = opts[1:]

            # Assign the next value in the options to the current space.
            # (Or let this happen in the main `solve` function?)
            self.board[prev_space] = self.options[prev_space][0]

            return prev_space


    def solve(self) -> None:
        ''' Solves the current board. '''

        # def _print(text):
        #     if __print:
        #         print(text)

        i = 0
        while i < len(self.board):
            j = 0
            while j < len(self.board):

                if self.__print: print("")

                space = (i,j)
                if self.__print: print(f"(solve) `space`: {space}")
                
                space_value = self.board[space]
                if self.__print: print(f"(solve) `space_value`: {space_value}")

                # if the space has a value, or the space is
                # if (space_value != 0) or (not (i,j) in self.board.clues):
                if space_value == 0:

                    # Find the options for this particular space.
                    space_options = self.board.get_options(i,j)
                    if self.__print: print(f"(solve) `space_options`: {space_options}")

                    if len(space_options) != 0:
                        # Get the first option and assign it
                        self.board[space] = space_options[0]

                        if self.__print: print(f"(solve) assigning {space} with value {space_options[0]}")
                        # Update self.options with the options that the current space had at the time.
                        # This is used when backtracking
                        self.options[space] = space_options

                    else: # len(options) == 0
                        # Backtrack here!
                        # Here, there are no valid options for the space with coordinates (i,j).
                        # That means we need to go back to the previous (non-clue) space and try the next valid value.
                        i,j = self.backtrack(i,j)
                        continue
                
                elif space in self.board.clues:
                    if self.__print: print("(solve) `space` is a clue. Skipping to next space")
                
                # else:
                    # Probably arrived here just after backtracking.
                    # Just carry on
                    # _print("Wtf happened here?")
                    # raise Exception

                if self.__print: print("")

                j += 1
            i += 1

        self.board.is_full = True

# ==============================

def main():
    solver = Backtracking()
    solver.solve()
    solver.board.conclude()

# ==============================

if __name__ == "__main__":
    main()
