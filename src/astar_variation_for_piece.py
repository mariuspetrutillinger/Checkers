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
                    return exist
        elif piece.player == self.color:
            for move in possible_moves:
                if piece.row > move[0] and board.board[move[0]][move[1]] != None and board.board[move[0]][move[1]].player != piece.player:
                    exist = True
                    return exist

        return exist

    # function to get the heuristic value of a piece
    def heuristic(self, piece):
        return -piece.score

    def simple_board_heuristic(self, board):
        player_pieces = board.get_all_pieces(self.color)
        opponent_pieces = board.get_all_pieces(3-self.color)

        return len(opponent_pieces) - len(player_pieces)

    def f_score(self, board, piece):
        return self.simple_board_heuristic(board) + self.heuristic(piece)

    # function to build the path for the ida_star algorithm
    def build_path(self, board, piece, limit):
        if self.goal_test(board, piece):
            print(("->").join([str(pos) for pos in piece.positions]))
            return (True, 0)

        f = self.f_score(board, piece)

        if limit < f:
            return (False, f)

        minim = float('inf')
        succesors = self.get_succesors_of_piece(board, piece)
        for succesor in succesors:
            new_board = deepcopy(board)
            if new_board.board[succesor[0]][succesor[1]] != None or (piece.is_valid_move((succesor[0], succesor[1])) == False):
                continue
            try:
                new_board.move_piece(piece, (succesor[0], succesor[1]))
                new_piece = new_board.board[succesor[0]][succesor[1]]
                piece.positions.append((succesor[0], succesor[1]))
                result, new_limit = self.build_path(new_board, new_piece, limit)
            except:
                continue

            if result:
                return (True, 0)
            
            piece.positions.pop()
            last_position = piece.positions[-1]
            piece.row = last_position[0]
            piece.col = last_position[1]
            board.board[last_position[0]][last_position[1]] = piece

            minim = min(minim, new_limit)

        return (False, minim)


    # function to apply the ida_star algorithm
    def ida_star(self, piece):
        piece.positions = [(piece.row, piece.col)]
        is_king = piece.king
        depth = self.f_score(self.game_board, piece)

        while True:
            result, limit = self.build_path(self.game_board, piece, depth)

            if result:
                first_position = piece.positions[0]
                piece.row = first_position[0]
                piece.col = first_position[1]
                piece.king = is_king
                return "Result found"
            depth = limit

            if limit == float('inf'):
                first_position = piece.positions[0]
                piece.row = first_position[0]
                piece.col = first_position[1]
                piece.king = is_king
                print("No result found")
                return "No result found"

            depth = limit

    # function to update the game board
    def update(self, game_board):
        self.game_board = deepcopy(game_board)