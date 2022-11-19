import sys
import os
import time
import json
import threading

from pprint import PrettyPrinter
pp = PrettyPrinter(indent=4)

sys.path.append(os.getcwd())
sys.path.append(os.getcwd() + "/src")

from src.board import Board
from src.algorithms.backtracking import Backtracking
from src.algorithms.stochastic_search import StochasticSearch

algorithms = [
    Backtracking,
    StochasticSearch
]

class Driver:

    def __init__(self):
        self.boards = []
        pass

    def generate_board(self):
        return Board().spaces

    @staticmethod
    def solve(solver):
        solver.solve()

    def do(self, algo: 'Backtracking|StochasticSearch'):

        # Instance of an algorithm, e.g. Backtracking
        solver = algo(self.generate_board())

        start_time = time.time()

        thread = threading.Thread(target=Driver.solve, args=(solver,), daemon=True)
        thread.start()

        while thread.is_alive():
            if time.time()-start_time > 10:
                print("Not handling this board well...")
                print(solver.board.initial_board)
                print()
                # TODO: write function to store problematic boards in boards.json
                sys.exit()

        end_time = time.time()

        time_taken = end_time-start_time

        solved = solver.board.is_complete()

        if solved:
            print("solved")
            Driver.conclude(board,solver.board, algo.__name__, time_taken)
            Driver.write_to_file(True,)
        else:
            print("not solved")


    @staticmethod
    def conclude(initial_board: 'list[list[int]]', finished_board: 'Board'):
        if finished_board.is_complete():

            print("\nBoard solved!")
            for index, (row1, row2) in enumerate(zip(initial_board, finished_board.spaces)):
                separator = " ---> " if index == 4 else "      "
                print(row1 + separator + row2)
            print()

        else:
            print("Board not complete")

    
    @staticmethod
    # def write_to_file(finished_board):
    def write_to_file(successful:'int', initial_board: 'list[list[int]]', finished_board: 'Board', algo_name:'str', time_taken:'float' = None):
        ''' Writes to `boards.json` file which contains data on boards solved '''

        # if not finished_board.is_complete():
        #     return

        ''' Get the contents of boards.json and put it into a python 'dict' '''

        boards = None

        try:
            with open("boards.json", "r") as infile:
                boards = json.load(infile)
        except:
            boards = {}

        # if successful:

        ''' Insert into 'boards' '''

        # Flag -- indicates whether the current initial_board is in the file
        initial_board_in_file = False

        '''
        In the "successful" section (a 'list'), each object will look like this:
        {
            "initial_board": <2D 'list' of integers>,
            "board_solutions": [{
                "algorithm": <the name of the algorithm, e.g. "Backtracking">,
                "solution": <2D 'list' of integers>,
                "time_taken": <float>
            }]
        }

        In the "unsuccessful" section (a 'list'), each object will look like this:

        {
            "initial_board": <2D 'list' of integers>,
            "algorithms_tried": [
                <the name of the algorithm, e.g. "Backtracking">
            ]
        }
        '''

        if successful:

            '''
            - We iterate through each entry in 'boards["unsuccessful"]' to see if
            the current 'initial_board' has already been solved.
                - If it has, we iterate through 'board_solutions' to see if the current solution/algorithm pair is in one of the entries
                    - If it is, we check whether to update the time_taken to its lowest
                    - Else, we add a new entry to 'board_solutions' containing the 'algorithm', 'solution' and 'time_taken'
                      that were passed into this function.
                - If it isn't, add a new entry, and check to see if the 'initial_board' was in boards["unsuccessful"]
                    - If it was, remove the 'algo_name' from "algorithms_tried"
            '''
            
            # Iterate through boards["successful"] to see if we find an entry whose
            # "initial_board" property is the same as the 'initial_board' parameter.
            for i1, entry in enumerate(boards["successful"]):

                if initial_board == entry["initial_board"]:
                    print("Found the initial_board parameter in boards.json")
                    
                    # So we found 'initial_board'. Now we iterate through each solution
                    # for this particular board to find if there's a solution whose "algorithm" and "solution" 
                    # properties match the 'algo_name' and 'finished_board.spaces' parameters.
                    for i2, existing_solution in enumerate(entry["board_solutions"]):

                        condition1 = (existing_solution["algorithm"] == algo_name)
                        condition2 = (existing_solution["solution"]  == finished_board) # finished_board.spaces
                        
                        print('(existing_solution["algorithm"] == algo_name)', condition1)
                        print('(existing_solution["solution"] == finished_board.spaces)', condition2)

                        # If the params match this existing solution's algorithm and space assignments
                        if condition1 and condition2:
                            # Now check to see if we should update the solution's "time_taken"
                            if time_taken < existing_solution["time_taken"]:
                                boards["successful"][i1]["board_solutions"][i2]["time_taken"] = time_taken
                            break
                        
                    # There isn't an existing solution in 'entry["board_solutions"]' with the same solution and algo_name.
                    # So add a new entry, and then check for a corresponding entry in boards["unsuccessful"].
                    else:
                        new_entry = {
                            "algorithm": algo_name,
                            "solution": finished_board.spaces,
                            "time_taken": time_taken
                        }
                        boards["successful"][i1]["board_solutions"].append(new_entry)

                        for i3, entry2 in enumerate(boards["unsuccessful"]):
                            if initial_board == entry2["initial_board"]:
                                del boards["unsuccessful"][i3]
                                break


                    break
            else:
                # Add a new entry to boards["successful"].
                # Also, need to check to see if 'initial_board' is in boards["unsuccessful"]
                print("Didn't find the initial_board parameter in boards.json")

        else:
            pp.pprint(boards['unsuccessful'])

            '''
            - We iterate through the "unsuccessful" section to see if the 'initial_board'
            is there.
                - If it is, we check to see if the algorithm that was just tried is 
            in the "algorithms_tried" section.
                    - If it is, we add it
                    - Else, we don't
                - Else, we add a whole new entry to the 'boards['unsuccessful']' 'list'
                containing the data passed into this function.
            
            '''

            for index, entry in enumerate(boards["unsuccessful"]):
                stored_initial_board = entry["initial_board"]
                stored_algos_tried = entry["algorithms_tried"]

                if initial_board == stored_initial_board:
                    # So the 'initial_board' that we just tried is already in 'boards.json'.
                    # Now check if 'algo_name' is in stored_algos_tried. And if it isn't add it.
                    if not algo_name in stored_algos_tried:
                        boards["unsuccessful"][index]["algorithms_tried"].append(algo_name)
                        # stored_algos_tried.append(algo_name)
                    break
                
            else:
                # The initial board isn't in 'boards.json'.
                # So we need to add a new 'dict' to 'boards'
                new_entry = {
                    "initial_board": initial_board,
                    "algorithms_tried": [algo_name]
                }
                boards["unsuccessful"].append(new_entry)

            print()
            pp.pprint(boards["unsuccessful"])
            print()
        
        # with open("boards.json", "w") as outfile:
        #     json.dump(boards,outfile)

if __name__ == "__main__":
    # Driver().do(Backtracking)
    # Driver.write_to_file(False, None, None, None, None)
    # Driver.write_to_file(
    #     True,
    #     [
    #         [0,0,0,0,0,5,0,0,3],
    #         [0,0,3,0,0,0,2,0,0],
    #         [0,0,0,0,0,0,0,0,0],
    #         [0,1,0,0,4,0,0,0,0],
    #         [0,0,0,0,5,0,0,1,2],
    #         [0,0,0,0,8,0,4,0,0],
    #         [0,0,5,0,0,0,0,0,0],
    #         [0,4,0,2,0,0,6,0,0],
    #         [7,0,6,0,0,0,0,0,0]
    #     ],
    #     [
    #         [1,2,4,6,7,5,8,9,3],
    #         [5,6,3,1,9,8,2,4,7],
    #         [8,7,9,4,2,3,1,5,6],
    #         [3,1,7,9,4,2,5,6,8],
    #         [4,9,8,3,5,6,7,1,2],
    #         [6,5,2,7,8,1,4,3,9],
    #         [2,3,5,8,6,4,9,7,1],
    #         [9,4,1,2,3,7,6,8,5],
    #         [7,8,6,5,1,9,3,2,4]
    #     ],
    #     "Backtracking",
    #     0.30303311347961426
    # )
    pass