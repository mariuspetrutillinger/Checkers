from game_setup import create_setup
from pygame_setup import game_loop

if (__name__ == "__main__"):
    algorithm, difficulty, color = create_setup()
    game_loop(algorithm, difficulty, color)