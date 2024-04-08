import pygame
from board import GameBoard

def game_loop():
    game_board = GameBoard()
    print ("Player's turn")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                game_board.handle_mouse_click(x, y)

        game_board.draw_board()
        game_board.draw_pieces()
        # Add more game logic here (handling moves, checking for game over, etc.)

        pygame.display.update()