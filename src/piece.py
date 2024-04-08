from constants import *
import pygame

class Piece:
    def __init__(self, row, col, player):
        self.row = row
        self.col = col
        self.player = player
        self.king = False

        if self.player == 1:
            self.direction = -1
        else:
            self.direction = 1

    def make_king(self):
        self.king = True

    def draw(self, screen):
        color = MAX_COLOR if self.player == 1 else MIN_COLOR
        pygame.draw.circle(screen, color, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2), PIECE_RADIUS)
        if self.king:
            color = MAX_KING_COLOR if self.player == 1 else MIN_KING_COLOR
            pygame.draw.circle(screen, color, (self.col * SQUARE_SIZE + SQUARE_SIZE // 2, self.row * SQUARE_SIZE + SQUARE_SIZE // 2), PIECE_RADIUS // 2, 5)

    def is_valid_move(self, end, capture=False):
        start_row, start_col = self.row, self.col
        end_row, end_col = end
        if self.king:
            if capture:
                return abs(end_row - start_row) == abs(end_col - start_col) == 2
            else:
                return abs(end_row - start_row) == abs(end_col - start_col) == 1
        if self.player == 1:
            if capture:
                return end_row - start_row == -2 and abs(end_col - start_col) == 2;
            else:
                return end_row - start_row == -1 and abs(end_col - start_col) == 1;
        else:
            if capture:
                return end_row - start_row == 2 and abs(end_col - start_col) == 2;
            else:
                return end_row - start_row == 1 and abs(end_col - start_col) == 1;

    def __repr__(self):
        return f"Piece({self.row}, {self.col}, {self.player})"

    def __str__(self):
        return f"Piece at ({self.row}, {self.col})"