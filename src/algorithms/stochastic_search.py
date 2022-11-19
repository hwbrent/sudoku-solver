import sys
import os

sys.path.append(os.getcwd())
sys.path.append(os.getcwd() + "/src")

from src.algorithms.algorithm import Algorithm
from src.board import Board

class StochasticSearch(Algorithm):
    
    def __init__(self, board):
        super().__init__(board)

    def solve(self):
        pass
