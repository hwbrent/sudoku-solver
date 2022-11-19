import abc
import copy
import sys
import os

sys.path.append(os.getcwd())
sys.path.append(os.getcwd() + "/src")

from src.board import Board

class Algorithm(abc.ABC):

    @abc.abstractmethod
    def __init__(self, board) -> 'None':
        self.initial_board = board
        self.board = copy.deepcopy(Board(board))

    @abc.abstractmethod
    def solve(self) -> 'bool':
        pass
