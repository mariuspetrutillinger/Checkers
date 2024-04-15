from constants import *
from board import GameBoard
from copy import deepcopy

class AI:
    # Function to initialize the AI
    # The AI will mainly play with red pieces (player 2)
    def __init__(self, player, game_board, depth):
        self.player = player
        self.game_board = deepcopy(game_board)
        self.depth = depth

    # Function to evaluate the board state
    def evaluate(self):
        if self.player == 1:
            return self.game_board.red_pieces - self.game_board.black_pieces + 0.5 * (self.game_board.red_kings - self.game_board.black_kings)
        else:
            return self.game_board.black_pieces - self.game_board.red_pieces + 0.5 * (self.game_board.black_kings - self.game_board.red_kings)

    # Function to get all possible moves for the AI
    def get_all_moves(self):
        all_moves = self.game_board.get_all_moves(self.player)
        return all_moves
    
    # Function for minimax algorithm 
    def minimax(self, board, depth, player):
        if depth == 0 or board.winner() != None:
            return self.evaluate(), None

        if player == 2:
            min_eval = float("inf")
            best_move = None
            for move in self.get_all_moves():
                evaluation = self.minimax(board, depth - 1, 1)[0]
                min_eval = min(min_eval, evaluation)
                if min_eval == evaluation:
                    best_move = move
            
            print ("min eval si best move")
            print (min_eval, best_move)
            return min_eval, best_move

        else:
            max_eval = float("-inf")
            best_move = None
            for move in self.get_all_moves():
                evaluation = self.minimax(board, depth - 1, 2)[0]
                max_eval = max(max_eval, evaluation)
                if max_eval == evaluation:
                    best_move = move
            
            print ("max eval si best move")
            print (max_eval, best_move)
            return max_eval, best_move

    # Function to make a move
    def make_move(self):
        move = self.minimax(self.game_board, self.depth, self.player)[1]
        if move == None:
            return
        start_row, start_col, end_pos = move
        if abs(start_row - end_pos[0]) == 1:
            self.game_board.move_piece(self.game_board.board[start_row][start_col], end_pos)
        elif abs(start_row - end_pos[0]) == 2:
            self.game_board.capture_piece(self.game_board.board[start_row][start_col], end_pos)
            middle_row, middle_col = self.game_board.get_middle_position((start_row, start_col), end_pos)
            print (self.game_board.board[middle_row][middle_col])
    
    def update(self, game_board):
        self.game_board = deepcopy(game_board)

    def __repr__(self):
        return f"AI({self.player}, {self.depth})"

    def __str__(self):
        return f"AI board state: {self.game_board}"