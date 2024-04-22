from constants import *
from board import GameBoard
from copy import deepcopy
import random

class AI:
    # Function to initialize the AI
    def __init__(self, player, game_board, depth, color):
        self.player = player
        self.game_board = deepcopy(game_board)
        self.depth = depth * 2
        self.color = color

    # Function to evaluate the board state
    def evaluate_by_piece_number(self):
        if self.player == 1:
            return self.game_board.red_pieces - self.game_board.black_pieces + 2 * (self.game_board.red_kings - self.game_board.black_kings)
        else:
            return self.game_board.black_pieces - self.game_board.red_pieces + 2 * (self.game_board.black_kings - self.game_board.red_kings)
        
    # Second function to evaluate the board state and establish a score
    def evaluate_by_composite(self):
        # the score will be determined using a composite of the number of pieces, the number of kings, and the position of the pieces
        # first we will initialize the score with the number of pieces and kings
        red_score = self.game_board.red_pieces + 2 * self.game_board.red_kings
        black_score = self.game_board.black_pieces + 2 * self.game_board.black_kings

        # as the game progresses, the position of the pieces will become more important
        # we will add the row number of the pieces to the score
        # because as the pieces move forward, they become more valuable being more versatile in their moves
        if self.color == 1:
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if self.game_board.board[row][col] != None:
                        if self.game_board.board[row][col].player == 1:
                            black_score += BOARD_SIZE - 1 - row
                        else:
                            red_score += row
        else:
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if self.game_board.board[row][col] != None:
                        if self.game_board.board[row][col].player == 2:
                            red_score += BOARD_SIZE - 1 - row
                        else:
                            black_score += row

        black_pieces = self.game_board.get_all_pieces(1)
        red_pieces = self.game_board.get_all_pieces(2)

        # we will also add a bonus to the score if the pieces are on the edges of the board
        # as the pieces at the left and right edges are defended and able to take other pieces more easily
        # and the pieces at the starting position are able to defend and not let the enemy have kings
        for piece in black_pieces:
            if piece[1] == 0 or piece[1] == BOARD_SIZE - 1:
                black_score += 5

            if piece[0] == 0:
                black_score += 10
            
        for piece in red_pieces:
            if piece[1] == 0 or piece[1] == BOARD_SIZE - 1:
                red_score += 5
            
            if piece[0] == BOARD_SIZE - 1:
                red_score += 10

        

        if self.player == 1:
            return red_score - black_score
        else:
            return black_score - red_score

    # Function to get the evaluation from the board score
    def evaluate_by_board_score(self, game_board):
        return game_board.get_board_score()

    # Function for getting all mvoes and their respective boards after the move
    def get_all_moves_and_boards(self, board, player):
        all_moves_and_boards = []
        all_moves = self.game_board.get_all_moves(player)
        random.shuffle(all_moves)

        for move in all_moves:
            new_board = deepcopy(board)
            self.act_move(new_board, move)
            all_moves_and_boards.append([new_board, move])

        return all_moves_and_boards

    # Function for minimax algorithm with alpha beta pruning
    def minimax_alpha_beta(self, position, depth, player, alpha, beta):
        if depth == 0 or position[0].winner() != None:
            return self.evaluate_by_board_score(position[0]), None

        if player == 2:
            min_eval = float("inf")
            best_move = None
            for move in self.get_all_moves_and_boards(position[0], player):
                evaluation = self.minimax_alpha_beta(move, depth - 1, 1, alpha, beta)[0]
                min_eval = min(min_eval, evaluation)
                if min_eval == evaluation:
                    best_move = move
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            
            return min_eval, best_move

        else:
            max_eval = float("-inf")
            best_move = None
            for move in self.get_all_moves_and_boards(position[0], player):
                evaluation = self.minimax_alpha_beta(move, depth - 1, 2, alpha, beta)[0]
                max_eval = max(max_eval, evaluation)
                if max_eval == evaluation:
                    best_move = move
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            
            return max_eval, best_move

    # Function to make a move for the ai based on the best move found by the minimax algorithm
    def make_move(self):
        move = self.minimax_alpha_beta([self.game_board, None], self.depth, self.player, float("-inf"), float("inf"))[1][1]
        if move == None:
            return
        start_row, start_col, end_pos = move
        if abs(start_row - end_pos[0]) == 1:
            print ("AI made normal move")
            self.game_board.move_piece(self.game_board.board[start_row][start_col], end_pos)
        elif abs(start_row - end_pos[0]) == 2:
            print ("AI made capture move")
            self.game_board.capture_piece(self.game_board.board[start_row][start_col], end_pos)

    def act_move(self, board, move):
        if move != None:
            start_row, start_col, end_pos = move
            piece = board.board[start_row][start_col]
            if piece is not None:
                if abs(start_row - end_pos[0]) == 1:
                    try:
                        board.move_piece(board.board[start_row][start_col], end_pos)
                    except:
                        return
                elif abs(start_row - end_pos[0]) == 2:
                    try:
                        board.capture_piece(board.board[start_row][start_col], end_pos)
                    except:
                        return
    
    def update(self, game_board):
        self.game_board = deepcopy(game_board)

    def __repr__(self):
        return f"AI({self.player}, {self.depth})"

    def __str__(self):
        return f"AI board state: {self.game_board}"