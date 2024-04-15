import pygame
import time
from board import GameBoard
from ai import AI
from constants import *

pygame.init()
pygame.display.set_caption('Checkers Game')
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))

# Function to draw the board
def draw_board():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = BOARD_COLOR_1 if (row + col) % 2 == 0 else BOARD_COLOR_2
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

# Function to draw the pieces
def draw_pieces(game_board):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if game_board.board[row][col] != None:
                game_board.board[row][col].draw(screen)

# Function to start the game, run the game and check for events
def game_loop():
    main_board = GameBoard()
    ai = AI(2, main_board, 3)
    print ("Player's turn")
    start_time = time.time()
    while main_board.winner() == None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print (f"Time taken: {time.time() - start_time}")
                return
            if main_board.current_player == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    main_board.handle_mouse_click(x, y)
                    ai.update(main_board)
            else:
                print ("AI's turn")
                ai.make_move()
                main_board.update(ai.game_board)
                print ("Player's turn")
        
        draw_board()
        draw_pieces(main_board)
        pygame.display.update()
        

    if main_board.winner() == 1:
        print ("Player wins")
    elif main_board.winner() == 2:
        print ("AI wins")

    print (f"Time taken: {time.time() - start_time}")