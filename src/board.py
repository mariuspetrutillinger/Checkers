from constants import *
import pygame
from piece import Piece

class GameBoard:
    pygame.init()

    pygame.display.set_caption('Checkers Game')

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.selected_piece = None
        self.current_player = 1
        self.black_pieces = 12
        self.red_pieces = 12

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if row < 3 and (row + col) % 2 == 1:
                    self.board[row][col] = Piece(row, col, 2)  # AI's pieces
                elif row > 4 and (row + col) % 2 == 1:
                    self.board[row][col] = Piece(row, col, 1)  # Player 1's pieces

    # Functions for drawing the board and pieces acording to the initial state of the game
    def draw_board(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if (row + col) % 2 == 0:
                    color = BOARD_COLOR_1
                else:
                    color = BOARD_COLOR_2
                pygame.draw.rect(self.screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
    def draw_pieces(self):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] != None:
                    self.board[row][col].draw(self.screen)

    # Function to handle mouse clicks
    def handle_mouse_click(self, x, y):
        row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
        print ("Move to row: ", row, " col: ", col)
        if self.selected_piece:
            if self.selected_piece.is_valid_move((row, col)):
                self.move_piece(self.selected_piece, (row, col))
                self.selected_piece = None
            else:
                print("Invalid move")
                self.selected_piece = None

        if self.board[row][col] != None and self.board[row][col].player == self.current_player:
            self.selected_piece = self.board[row][col]
        
    # Function to move a piece
    def move_piece(self, piece, end):
        start_row, start_col = piece.row, piece.col
        end_row, end_col = end

        print ("Moving piece from row: ", start_row, " col: ", start_col, " to row: ", end_row, " col: ", end_col)

        capture = piece.is_valid_move(end, True)

        if self.board[start_row][start_col].player == self.current_player and self.board[end_row][end_col] == None and (piece.is_valid_move(end) or capture):
            if capture:
                captured_row, captured_col = self.capture_piece((start_row, start_col), (end_row, end_col))
                if self.board[captured_row][captured_col].player == 1:
                    self.black_pieces -= 1
                else:
                    self.red_pieces -= 1
                self.board[captured_row][captured_col] = None

            self.board[end_row][end_col] = self.board[start_row][start_col]
            self.board[start_row][start_col] = None
            self.board[end_row][end_col].row = end_row
            self.board[end_row][end_col].col = end_col

            if end_row == 0 or end_row == 7:
                self.board[end_row][end_col].make_king()

            self.current_player = 1 if self.current_player == 2 else 2

    
    def capture_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        return (start_row + end_row) // 2, (start_col + end_col) // 2
        
    def __repr__(self):
        return f"GameBoard({self.board})"
    
    def __str__(self):
        return f"GameBoard with board: {self.board}"