import pygame
from copy import deepcopy
from constants import *
from piece import Piece

# Class to represent the game board
# The board is represented as a 2D list where each element is a Piece object
# This class also serves as a state of the game
class GameBoard:
    # Function to initialize the game board
    def __init__(self, color):
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.selected_piece = None
        self.mandatory_capture_pieces = []
        self.current_player = 1
        self.black_pieces = 12
        self.red_pieces = 12
        self.black_kings = 0
        self.red_kings = 0
        self.color = color
        self.board_score = 0

        # building the board will be different depending on wether the player is playing with red or black pieces
        if color == 1:
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if row < 3 and (row + col) % 2 == 1:
                        self.board[row][col] = Piece(row, col, 2, color)  # AI's pieces
                    elif row > 4 and (row + col) % 2 == 1:
                        self.board[row][col] = Piece(row, col, 1, color)  # Player 1's pieces
        elif color == 2:
            for row in range(BOARD_SIZE):
                for col in range(BOARD_SIZE):
                    if row < 3 and (row + col) % 2 == 1:
                        self.board[row][col] = Piece(row, col, 1, color)  # AI's pieces
                    elif row > 4 and (row + col) % 2 == 1:
                        self.board[row][col] = Piece(row, col, 2, color)  # Player 1's pieces
        
        self.board_score = self.get_board_score()

    # Function to handle mouse clicks, assign the selected piece and move it if possible
    def handle_mouse_click(self, x, y):
        row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
        print (self)
        if self.selected_piece:
            if self.mandatory_capture_pieces and (row, col) in self.mandatory_capture_pieces:
                self.capture_piece(self.selected_piece, (row, col))
                self.mandatory_capture_pieces = []
                self.selected_piece = None
            elif self.mandatory_capture_pieces and (row, col) not in self.mandatory_capture_pieces:
                print ("You need to capture a piece")
                self.selected_piece = None
            else:
                try:
                    self.move_piece(self.selected_piece, (row, col))
                    self.selected_piece = None
                except:
                    print ("Invalid move. Try again")

        if self.board[row][col] != None and self.board[row][col].player == self.current_player:
            self.selected_piece = self.board[row][col]
            self.mandatory_capture_pieces = self.mandatory_capture(self.selected_piece)
        
    # Function to move a piece if possible, check if the piece becomes a king and change the turn
    def move_piece(self, piece, end, capture=False):
        start_row, start_col = piece.row, piece.col
        end_row, end_col = end

        # when a move piece action is engaged we check if the move is possible
        move_possible = piece.is_valid_move(end, capture)
        # if the move is possible and the space we want to move to is empty then we will change
        # the values of the end position to match the piece we wanted to move
        # and see whether the piece has reached the end of the board to become a king
        if move_possible and self.board[end_row][end_col] == None:
            self.board[end_row][end_col] = piece
            self.board[start_row][start_col] = None
            self.board[end_row][end_col].row = end_row
            self.board[end_row][end_col].col = end_col

            if end_row == 0 or end_row == 7:
                self.board[end_row][end_col].make_king()
                if self.board[end_row][end_col].player == 1:
                    self.black_kings += 1
                else:
                    self.red_kings += 1

            # at the end if the move was succesful we will change the turn and update the board score
            self.current_player = 1 if self.current_player == 2 else 2
        else:
            raise Exception("Invalid move")

    # Function used to "capture" a piece
    def capture_piece(self, piece, end):
        capture_row, capture_col = self.get_middle_position((piece.row, piece.col), end)
        try:
            self.move_piece(piece, end, True)
            self.board[capture_row][capture_col] = None
        except:
            print ("Invalid capture move")
        if self.current_player == 1:
            self.black_pieces -= 1
        else:
            self.red_pieces -= 1
        
    # Function to check if a move is valid for capture
    def is_capture_move(self, piece, end):
        end_row, end_col = end
        if not piece.king:
            if self.color == 1:
                if piece.player == 1:
                    if end_row > piece.row:
                        return False
                elif piece.player == 2:
                    if end_row < piece.row:
                        return False
            elif self.color == 2:
                if piece.player == 1:
                    if end_row < piece.row:
                        return False
                elif piece.player == 2:
                    if end_row > piece.row:
                        return False

        middle_row, middle_col = self.get_middle_position((piece.row, piece.col), end)
        if self.board[end_row][end_col] == None and self.board[middle_row][middle_col] != None and self.board[middle_row][middle_col].player != piece.player:
            return True
        
        return False

    # Function to get all capture moves for a piece if there are any
    # If there are any capture moves, the player must make a capture move and cannot make a normal move (for a specific piece)
    def mandatory_capture(self, piece):
        capture_list = []
        row, col = piece.row, piece.col
        possible_moves = [(row + 2, col + 2), (row + 2, col - 2), (row - 2, col + 2), (row - 2, col - 2)]
        possible_moves = [(r, c) for r, c in possible_moves if r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE]
        if piece.king:
            for move in possible_moves:
                if self.is_capture_move(piece, move):
                    capture_list.append(move)
        else:
            for move in possible_moves:
                if self.is_capture_move(piece, move):
                    capture_list.append(move)
        
        return capture_list
    
    # Function to get the middle position between two positions used to handle captures
    def get_middle_position(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        return (start_row + end_row) // 2, (start_col + end_col) // 2

    # Function to get all possible moves for a player (normal and capture moves) as they will serve as succesors for the current state
    def get_all_moves(self, player):
        all_moves = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] != None and self.board[row][col].player == player:
                    all_moves.extend([(row, col, move) for move in self.get_valid_moves(self.board[row][col])])
                    all_moves.extend([(row, col, move) for move in self.mandatory_capture(self.board[row][col])])
        
        return all_moves
    
    # Function to get all normal moves for a piece
    def get_valid_moves(self, piece):
        valid_moves = []
        row, col = piece.row, piece.col
        # we are getting a list of all possible moves that can be split for moves that are upwards and downwards
        possible_moves = [(row + 1, col + 1), (row + 1, col - 1), (row - 1, col + 1), (row - 1, col - 1)]
        possible_moves = [(r, c) for r, c in possible_moves if r >= 0 and r < BOARD_SIZE and c >= 0 and c < BOARD_SIZE]
        
        # depending on the side we are playing on and the type of piece we are moving we will get the valid moves
        if self.color == 1:
            if piece.king:
                for move in possible_moves:
                    if self.board[move[0]][move[1]] == None and piece.is_valid_move(move):
                        valid_moves.append(move)
            elif piece.player == 1:
                for move in possible_moves:
                    if piece.row > move[0] and self.board[move[0]][move[1]] == None and piece.is_valid_move(move):
                        valid_moves.append(move)
            else:
                for move in possible_moves:
                    if piece.row < move[0] and self.board[move[0]][move[1]] == None and piece.is_valid_move(move):
                        valid_moves.append(move)
        elif self.color == 2:
            if piece.king:
                for move in possible_moves:
                    if self.board[move[0]][move[1]] == None and piece.is_valid_move(move):
                        valid_moves.append(move)
            elif piece.player == 2:
                for move in possible_moves:
                    if piece.row > move[0] and self.board[move[0]][move[1]] == None and piece.is_valid_move(move):
                        valid_moves.append(move)
            else:
                for move in possible_moves:
                    if piece.row < move[0] and self.board[move[0]][move[1]] == None and piece.is_valid_move(move):
                        valid_moves.append(move)
        
        return valid_moves

    # Function to get all pieces for a player
    def get_all_pieces(self, player):
        pieces = []
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] != None and self.board[row][col].player == player:
                    pieces.append((row, col))
        
        return pieces

    # Function to return the winner of the game based on the number of pieces and the number of moves available
    def winner(self):
        if self.black_pieces == 0 and self.red_pieces != 0:
            return "Red"
        elif self.red_pieces == 0 and self.black_pieces != 0:
            return "Black"
        else:
            black_moves = self.get_all_moves(1)
            red_moves = self.get_all_moves(2) 

            if len(black_moves) == 0 and len(red_moves) == 0:
                return "Draw"
            elif len(black_moves) == 0:
                return "Red"
            elif len(red_moves) == 0:
                return "Black"

        return None    

    # Function to update the game board (used to update the image shown on screen as well as the information provided by the AI)
    def update(self, game_board):
        self.board = deepcopy(game_board.board)
        self.current_player = game_board.current_player
        self.black_pieces = game_board.black_pieces
        self.red_pieces = game_board.red_pieces
        self.black_kings = game_board.black_kings
        self.red_kings = game_board.red_kings
        self.board_score = game_board.board_score

    # Function to get the score of the board
    def get_board_score(self):
        board_score = 0
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] != None:
                    capture_potential = len(self.mandatory_capture(self.board[row][col]))
                    if self.board[row][col].player == 1:
                        board_score += self.board[row][col].score
                        board_score += capture_potential
                    else:
                        board_score -= self.board[row][col].score
                        board_score -= capture_potential

        return board_score

    def __repr__(self):
        return f"GameBoard({self.board})"
    
    # Function to print the board and the game state in the console
    def __str__(self):
        board_representation = ""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] is None:
                    board_representation += "- "
                else:
                    board_representation += str(self.board[row][col].player) + " "
            board_representation += "\n"
        return board_representation

    def __eq__(self, other):
        return self.board == other.board
    
    def __lt__ (self, other):
        return self.board_score < other.board_score

    def __hash__(self):
        return hash(str(self.board))
