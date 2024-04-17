from constants import *
import pygame

# Class to represent a piece on the board
class Piece:
    # Function to initialize the piece
    def __init__(self, row, col, player, color):
        self.row = row
        self.col = col
        self.player = player
        self.color = color
        self.king = False

        # we are going to add a new attribute to the Piece class called direction. 
        # this attribute will be used to determine the direction in which the piece can move. 
        if self.color == 1:
            if self.player == 1:
                self.direction = -1
            else:
                self.direction = 1
        else:
            if self.player == 1:
                self.direction = 1
            else:
                self.direction = -1

    # Function to make the piece a king
    def make_king(self):
        self.king = True

    # Function to draw the piece on the screen
    def draw(self, screen):
        color = MAX_COLOR if self.player == 1 else MIN_COLOR
        pygame.draw.circle(screen, color, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2), PIECE_RADIUS)
        if self.king:
            color = MAX_KING_COLOR if self.player == 1 else MIN_KING_COLOR
            pygame.draw.circle(screen, color, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2), PIECE_RADIUS // 2, 5)

    # Function to check if a move is valid for the piece using the difference in position and the direction of the piece
    def is_valid_move(self, end, capture=False):
        end_row, end_col = end
        row_diff = end_row - self.row
        col_diff = end_col - self.col

        if not capture:
            if abs(row_diff) != 1 or abs(col_diff) != 1:
                return False

            if not self.king and row_diff != self.direction:
                return False

        else:
            if abs(row_diff) != 2 or abs(col_diff) != 2:
                return False

            if not self.king and row_diff != 2 * self.direction:
                return False

        return True

    def __repr__(self):
        return f"Piece({self.row}, {self.col}, {self.player})"

    def __str__(self):
        return f"Piece at ({self.row}, {self.col})"