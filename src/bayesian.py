from constants import *
from board import GameBoard
from copy import deepcopy

# class to represent the Bayesian network
class Bayesian:
    def __init__(self, board, player, color):
        self.game_board = deepcopy(board)
        self.player = player
        self.color = color

    