from constants import *
from board import GameBoard
from copy import deepcopy
from queue import PriorityQueue

# class to represent the A* algorithm
class A_Star_for_piece:
    def __init__(self, game_board, player, color):
        self.game_board = game_board
        self.player = player
        self.color = color

    # function to get the succesors of a piece
    def get_succesors_of_piece(self, board, piece):
        succesors = []

        succesors.extend(board.get_valid_moves(piece))

        return succesors

    # function to test if goal has been reached
    def goal_test(self, board, piece):
        row, col = piece.row, piece.col
        exist = False

        possible_moves = [(row + 1, col + 1), (row + 1, col - 1), (row - 1, col + 1), (row - 1, col - 1)]
        possible_moves = [(r, c) for r, c in possible_moves if r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE]

        if piece.king:
            for move in possible_moves:
                if board.board[move[0]][move[1]] != None and board.board[move[0]][move[1]].player != piece.player:
                    exist = True
        elif piece.player == self.color:
            for move in possible_moves:
                if piece.row > move[0] and board.board[move[0]][move[1]] != None and board.board[move[0]][move[1]].player != piece.player:
                    exist = True

        return exist

    # function to get the heuristic value of a piece
    def heuristic(self, piece):
        return -piece.score

    # function to build the path for the ida_star algorithm
    def build_path(self, board, piece, limit):
        if self.goal_test(board, piece):
            print(("->").join([str(pos) for pos in piece.positions]))
            return (True, 0)

        if limit < self.heuristic(piece):
            return (False, self.heuristic(piece))

        minim = float('inf')
        for succesors in self.get_succesors_of_piece(board, piece):
            
            try:
                new_board = deepcopy(self.game_board)
                new_board.move_piece(piece, (succesors[0], succesors[1]))
                piece.positions.append((succesors[0], succesors[1]))
                new_piece = new_board.board[succesors[0]][succesors[1]]

                result, limit = self.build_path(new_board, new_piece, limit)
            except:
                return (False, 0)

            if result:
                return (True, 0)

            minim = min(minim, limit)

        return (False, minim)


    # function to apply the ida_star algorithm
    def ida_star(self, piece):
        piece.positions = [(piece.row, piece.col)]
        is_king = piece.king
        depth = self.heuristic(piece)

        while True:
            result, limit = self.build_path(self.game_board, piece, depth)

            if result:
                first_position = piece.positions[0]
                piece.row = first_position[0]
                piece.col = first_position[1]
                piece.king = is_king
                return "Result found"

            if limit == float('inf'):
                first_position = piece.positions[0]
                piece.row = first_position[0]
                piece.col = first_position[1]
                piece.king = is_king
                return "No result found"

            depth = limit

    # function to update the game board
    def update(self, game_board):
        self.game_board = deepcopy(game_board)