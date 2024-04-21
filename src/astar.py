from constants import *
from board import GameBoard
from copy import deepcopy
from queue import PriorityQueue

# class to represent the A* algorithm
class A_Star:
    def __init__(self, game_board, player, color):
        self.game_board = game_board
        self.player = player
        self.color = color

    # function to get the heuristic value of the board
    def heuristic(self):
        if self.player == 1:
            return self.game_board.red_pieces - self.game_board.black_pieces

        else:
            return self.game_board.black_pieces - self.game_board.red_pieces

    # function to get the distance between two board states
    def distance_between(self, current, neighbor):
        return 1

    # function to get the heuristic cost estimate
    def heuristic_cost_estimate(self, neighbor):
        if neighbor.current_player == 1:
            return neighbor.red_pieces - neighbor.black_pieces
        else:
            return neighbor.black_pieces - neighbor.red_pieces

    #function to make a move 
    def make_move(self, move):
        if move == None:
            return
        start_row, start_col, end_pos = move
        if abs(start_row - end_pos[0]) == 1:
            self.game_board.move_piece(self.game_board.board[start_row][start_col], end_pos)
        elif abs(start_row - end_pos[0]) == 2:
            self.game_board.capture_piece(self.game_board.board[start_row][start_col], end_pos)
    
    # function to get all neighbors of the current board state
    def get_neighbors(self):
        neighbors = []
        for move in self.game_board.get_all_moves(self.player):
            neighbor = deepcopy(self.game_board)
            start_row, start_col, end_pos = move
            if abs(start_row - end_pos[0]) == 1:
                neighbor.move_piece(neighbor.board[start_row][start_col], end_pos)
            elif abs(start_row - end_pos[0]) == 2:
                neighbor.capture_piece(neighbor.board[start_row][start_col], end_pos)
            neighbors.append(neighbor)
        return neighbors

    # function for the A* algorithm
    def a_star(self):
        closed_set = set()
        open_set = PriorityQueue()
        open_set.put((0, self.game_board))
        came_from = {}
        g_score = {self.game_board: 0}
        f_score = {self.game_board: self.heuristic()}
        while not open_set.empty():
            current = open_set.get()[1]
            if current.winner() != None:
                return current
            closed_set.add(current)
            for neighbor in self.get_neighbors():
                if neighbor in closed_set:
                    continue
                tentative_g_score = g_score[current] + self.distance_between(current, neighbor)
                if neighbor not in [item[1] for item in open_set.queue]:
                    open_set.put((tentative_g_score + self.heuristic_cost_estimate(neighbor), neighbor))
                elif tentative_g_score >= g_score[neighbor]:
                    continue
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + self.heuristic_cost_estimate(neighbor)
        return None

    # function to make a move based on the best move found by the A* algorithm
    def make_best_move(self):
        best_node = self.a_star()
        if best_node == None:
            return
        move = best_node.game_board.last_move
        self.make_move(move)
        self.game_board.update(best_node.game_board)
        print ("Player's turn")
    