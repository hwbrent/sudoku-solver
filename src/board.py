import copy
import random
import json
from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

# ==============================

class Board:
    '''
    Size: 9x9
    
    A 0 in a space denotes an empty space.
    '''

    # ---------------

    def __init__(self, board:'list[list[int]]|None' = None, __print:'bool' = False):
        ''' Allows for a `board` to be passed in. If not, it defaults to generating clues. '''

        self.is_full = False

        if board is None:
            self.spaces = [[0 for _ in range(9)] for _ in range(9)]
            self.clues = []
            self.__set_clues()
        else:
            self.spaces = board
            self.clues = []
            for i, row in enumerate(self.spaces):
                for j, entry in enumerate(row):
                    if entry != 0:
                        self.clues.append((i,j))

        self.initial_board = copy.deepcopy(self.spaces)
        self.__print = __print


    def __getitem__(self, key) -> 'list':
        if type(key) == tuple and len(key) == 2:
            return self.spaces[key[0]][key[1]]
        else:
            return self.spaces[key]
    

    def __setitem__(self,key,value) -> None:
        if type(key) == tuple:
            self.spaces[key[0]][key[1]] = value
        else:
            self.spaces[key] = value


    def __len__(self):
        return len(self.spaces)

    def __get_strings(self):
        ''' Formats the board into 9 grids. '''
        strings = ["\n"] # \n to give the top of the board a bit of breathing room

        for row_index, row in enumerate(self.spaces):
            row_string = ""

            row_string += " ".join([str(x) for x in row[:3]])
            row_string += " | "
            row_string += " ".join([str(x) for x in row[3:6]])
            row_string += " | "
            row_string += " ".join([str(x) for x in row[6:]])

            strings.append(row_string)
            
            if row_index in [2,5]:
                divider = "-" * len(row_string)
                strings.append(divider)

        return strings


    def __str__(self) -> 'str':
        return "\n".join(self.__get_strings())

    # ---------------

    def get_row(self, row_index:'int', column_index:'int') -> 'list':
        ''' Returns the row in `self.spaces` with index `row_index` (not including the value at `self.spaces[row_index][column_index]`). '''
        return [value for value_index, value in enumerate(self.spaces[row_index]) if value_index != column_index]


    def get_column(self, row_index_param:'int', column_index: 'int') -> 'list':
        return [row[column_index] for row_index, row in enumerate(self.spaces) if row_index != row_index_param]


    def get_grid(self, row_index:'int', column_index: 'int') -> 'list':
        
        row_third = None
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

                cond1 = (not c_index in column_third)
                cond2 = ((row_index, column_index) == (r_index, c_index))

                if not (cond1 or cond2):
                    grid_values.append(column_value)
        
        return grid_values

    
    def get_prev_space(self,i:'int',j:'int') -> 'tuple[int,int]':
        '''
        Gets the closest space behind `self.spaces[i][j]` not in `self.clues`.
        
        This is used in `Backtracking.backtrack`.
        '''

        for prev_i in reversed(range(i+1)): # because we don't want to see any rows further forward than (i,j)

            for prev_j in reversed(range(9)): # because we still need to see every value in each of the previous rows

                # skip past every further-on coordinate on the same row as (i,j)
                if prev_i == i and prev_j >= j:
                    continue

                if (prev_i, prev_j) in self.clues:
                    continue

                # print(prev_i, prev_j)
                return (prev_i, prev_j)

    # ---------------

    def is_empty(self, row_index:'int', column_index:'int') -> 'bool':
        ''' Indicates whether the space at `self.spaces[i][j]` has been allocated a value yet. '''
        if self.is_full:
            return True
        else:
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
    

    def get_options(self, i, j):
        return [x for x in range(1,10) if self.is_legal_in_space(x,i,j)]


    def is_complete(self) -> 'bool':
        '''
        Checks that every space in `self.spaces` has a value which isn't `0` and that the value assignment is valid.
        
        (Should only be called after `self.spaces` is thought to have been completed)
        '''

        for row_index, row in enumerate(self.spaces):
            for column_index, value in enumerate(row):
                space = (row_index, column_index)
                if (value == 0) or (not self.is_legal_in_space(value, *space)):
                    return False
        return True

    # ---------------

    def __set_clues(self) -> 'None':
        ''' Adds some randomly generated 'clues' to `self.spaces`. '''

        clues_added = 0

        while clues_added != 17:

            i = random.randint(0,8)
            j = random.randint(0,8)
            val = random.randint(1,10)

            if self.is_legal_in_space(val,i,j):
                self.spaces[i][j] = val
                self.clues.append((i,j))
                clues_added += 1

# ==============================
