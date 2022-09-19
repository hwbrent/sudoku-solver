import random
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=4)

class Board:
    '''
    Size: 9x9
    
    A 0 in a space denotes an empty space.
    '''

    # ---------------

    def __init__(self, board:'list[list[int]]|None' = None):
        ''' Allows for a `board` to be passed in. If not, it defaults to generating clues. '''

        if board is None:
            self.spaces = [[0 for _ in range(9)] for _ in range(9)]
            self.__set_clues()
            pp.pprint(self.spaces)
        else:
            self.spaces = board


    def __getitem__(self, key) -> 'list':
        return self.spaces[key]

    # ---------------

    def get_row(self, row_index:'int', column_index:'int') -> 'list':
        ''' Returns the row in `self.spaces` with index `row_index` (not including the value at `self.spaces[row_index][column_index]`). '''
        return [value for value_index, value in enumerate(self.spaces[row_index]) if value_index != column_index]


    def get_column(self, row_index_param:'int', column_index: 'int') -> 'list':
        return [row[column_index] for row_index, row in enumerate(self.spaces) if row_index != row_index_param]


    def get_grid(self, row_index:'int', column_index: 'int') -> 'list':
        
        row_third    = None
        column_third = None

        lower = 0
        upper = 3
        while upper <= 9:

            current_third = range(lower, upper)

            if row_index in current_third:
                row_third = current_third
            
            if column_index in current_third:
                column_third = current_third
            
            lower += 3
            upper += 3

        grid_values = []

        for r_index, row in enumerate(self.spaces):
            if not r_index in row_third:
                continue
            for c_index, column_value in enumerate(row):
                if not c_index in column_third:
                    continue
                grid_values.append(column_value)
        
        return grid_values

    # ---------------

    def is_empty(self, row_index:'int', column_index:'int') -> 'bool':
        ''' Indicates whether the space at `self.spaces[i][j]` has been allocated a value yet. '''
        return self.spaces[row_index][column_index] == 0


    def is_legal_in_space(self, value:'int', row_index:'int', column_index:'int') -> 'bool':
        '''
        Indicates whether `value` will be legal in the space `self.spaces[row_index][column_index]`.
        
        For `value` to be valid, it cannot already be present in the exact position, row, column or grid corresponding to `(row_index,column_index)`.
        '''

        row = self.get_row(row_index, column_index)
        column = self.get_column(row_index, column_index)
        grid = self.get_grid(row_index, column_index)

        cond1 = (self.is_empty(row_index, column_index))
        cond2 = (not value in row)
        cond3 = (not value in column)
        cond4 = (not value in grid)

        return cond1 and cond2 and cond3 and cond4

    # ---------------

    def __set_clues(self) -> 'None':
        ''' Adds some randomly generated 'clues' to `self.spaces`. '''

        clues_added = 0

        while clues_added != 17:

            i = random.randint(0,8)
            j = random.randint(0,8)
            val = random.randint(1,9)

            if self.is_legal_in_space(val,i,j):
                self.spaces[i][j] = val
                clues_added += 1

def main():
    board = Board()
    # print(Board().get_grid(8,8))

if __name__ == "__main__":
    main()
