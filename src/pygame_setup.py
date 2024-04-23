import pygame
import time
from board import GameBoard
from ai import AI
from astar_variation_for_piece import A_Star_for_piece
from copy import deepcopy
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
def game_loop(algorithm, difficulty, color):
    color = int(color)
    algorithm = int(algorithm)
    difficulty = int(difficulty)
    
    main_board = GameBoard(color)
    ai = AI(3-color, main_board, difficulty, color)
    astar = A_Star_for_piece(main_board, color, color)

    start_time = time.time()
    while main_board.winner() == None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print (f"Time taken: {time.time() - start_time}")
                return
            if main_board.current_player == color:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    main_board.handle_mouse_click(x, y)
                    if main_board.selected_piece != None:
                        copy_board = deepcopy(main_board)
                        astar.update(main_board)
                        print ("Ida path: ")
                        astar.ida_star(main_board.selected_piece)
                        main_board.update(astar.game_board)
                        main_board.update(copy_board)
                    ai.update(main_board)
            else:
                print ("AI's turn")
                ai.make_move()
                # print (ai.game_board)
                main_board.update(ai.game_board)
                print ("Player's turn")
        
        draw_board()
        draw_pieces(main_board)
        pygame.display.update()
        

    if main_board.winner() == "Draw":
        print ("Game is a draw")
    else:
        print (f"Player {main_board.winner()} wins")
    print (f"Score: {main_board.get_board_score()}")
    print (f"Time taken: {time.time() - start_time}")