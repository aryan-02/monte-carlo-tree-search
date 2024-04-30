from enum import IntEnum
import tictactoe
import maxConnect4
import random
from copy import deepcopy
import math

games = [tictactoe, maxConnect4]

class Game(IntEnum):
    TICTACTOE = 0
    MAXCONNECT4 = 1

class MCTSNode:
    def __init__(self, game, board, parent=None, move=None):
        self.game = game
        self.board = board
        self.parent = parent
        self.move = move
        self.win_counts = {
            game.player1: 0,
            game.player2: 0
        }
        self.num_rollouts = 0
        self.children = []
        self.unvisited_moves = list(game.actions(board))

    def add_random_child(self):
        index = random.randint(0, len(self.unvisited_moves) - 1)
        new_move = self.unvisited_moves.pop(index)
        new_game_state = self.game.result(self.board, new_move)
        new_node = MCTSNode(self.game, new_game_state, self, new_move)
        self.children.append(new_node)
        return new_node
    
    def record_win(self, winner):
        if winner is not None:
            self.win_counts[winner] += 1
        elif winner is None:
            self.win_counts[self.game.player1] += 0.5
            self.win_counts[self.game.player2] += 0.5
        self.num_rollouts += 1
    
    def can_add_child(self):
        return len(self.unvisited_moves) > 0
    
    def is_terminal(self):
        return self.game.terminal(self.board)

    def winning_frac(self, player):
        return float(self.win_counts[player]) / float(self.num_rollouts)


def uct_score(parent_rollouts, child_rollouts, win_pct, temperature):
    exploration = math.sqrt(math.log(parent_rollouts) / child_rollouts)
    return win_pct + temperature * exploration

class MCTSAgent:
    def __init__(self, game_e, num_rounds, temperature):
        self.game = games[int(game_e)]
        self.num_rounds = num_rounds
        self.temperature = temperature
    
    def simulate_random_game(self, board_in):
        board = deepcopy(board_in)
        while not self.game.terminal(board):
            moves_possible = self.game.actions(board)
            move = random.choice(list(moves_possible))
            board = self.game.result(board, move)
        
        return self.game.winner(board)
    
    def select_child(self, node):
        total_rollouts = sum(child.num_rollouts for child in node.children)
        
        best_score = -1
        best_child = None

        for child in node.children:
            score = uct_score(total_rollouts, child.num_rollouts, child.winning_frac(self.game.player(node.board)), self.temperature)
            if score > best_score:
                best_score = score
                best_child = child
        return best_child

    def select_move(self, board):
        # Build MCTS Tree
        root = MCTSNode(self.game, board)
        for i in range(self.num_rounds):
            node = root
            while (not node.can_add_child() and not node.is_terminal()):
                node = self.select_child(node)
            
            if node.can_add_child():
                node = node.add_random_child()
            
            winner = self.simulate_random_game(node.board)

            while node is not None:
                node.record_win(winner)
                node = node.parent
        # Pick the best move
        best_move = None
        best_pct = -1.0
        for child in root.children:
            child_pct = child.winning_frac(self.game.player(root.board))
            if child_pct > best_pct:
                best_pct = child_pct
                best_move = child.move
        
        return best_move
                        
            

def board_value(game, board, depth=100, alpha=-float('inf'), beta=float('inf')):
    if game.terminal(board):
        return game.utility(board)
    
    if depth == 0:
        return game.sbe(board)

    v = -float('inf') if game.player(board) == game.player1 else float('inf')

    for action in game.actions(board):
        res_board = game.result(board, action)
        if game.player(board) == game.player1:                                      # Maximizing Player
            v = max(v, board_value(game, res_board, depth - 1, alpha, beta))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        else:                                                                       # Minimizing Player
            v = min(v, board_value(game, res_board, depth - 1, alpha, beta))
            if v <= alpha:
                return v
            beta = min(beta, v)
    return v


def minimax_decision(game_e, board, depth = 100):
    """
    Returns the optimal action for the current player on the board.
    """
    game = games[int(game_e)]
    actions_possible = list(game.actions(board))
    boards_from_actions = [game.result(board, action) for action in actions_possible]
    values = [board_value(game, board, depth) for board in boards_from_actions]
    if(game.player(board) == game.player1):
        return actions_possible[values.index(max(values))]
    else:
        return actions_possible[values.index(min(values))]
    
