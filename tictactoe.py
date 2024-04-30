"""
Tic Tac Toe Model
"""

import math

from copy import deepcopy

X = "X"
O = "O"
EMPTY = None

player1 = X                     # Maximizing Player
player2 = O                     # Minimizing Player

def read_game_file(filename):
    """
    Reads a text file and returns the corresponding board array
    """
    with open(filename, 'r') as fh:
        board = []
        for line in fh.readlines():
            board_row = []
            for character in line:
                if character == 'X':
                    board_row.append(X)
                elif character == 'O':
                    board_row.append(O)
                elif character == '-':
                    board_row.append(EMPTY)
            board.append(board_row)
        return board

def write_game_file(board, filename):
    """
    Outputs the current board configuration to a text file.
    """
    with open(filename, 'w') as fh:
        for row in board:
            for col in row:
                if col == X:
                    fh.write('X')
                elif col == O:
                    fh.write('O')
                else:
                    fh.write('-')
            fh.write('\n')

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0
    for row in board:
        for item in row:
            if item == X:
                x_count += 1
            elif item == O:
                o_count += 1
    return O if x_count > o_count else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                action_set.add((i, j))
    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = deepcopy(board)
    i, j = action
    if board[i][j] is EMPTY:
        new_board[i][j] = player(board)
    else:
        raise ValueError("Invalid move.")
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check if X won
    x_won = False
    for row in board:
        if row.count(X) == 3:
            x_won = True
    
    for c in range(3):
        x_count = 0
        for r in range(3):
            if board[r][c] == X:
                x_count += 1
        if x_count == 3:
            x_won = True
    
    if board[0][0] == X and board[1][1] == X and board[2][2] == X:
        x_won = True
    elif board[0][2] == X and board[1][1] == X and board[2][0] == X:
        x_won = True
    
    # Check if O won
    o_won = False
    for row in board:
        if row.count(O) == 3:
            o_won = True
    
    for c in range(3):
        o_count = 0
        for r in range(3):
            if board[r][c] == O:
                o_count += 1
        if o_count == 3:
            o_won = True
    
    if board[0][0] == O and board[1][1] == O and board[2][2] == O:
        o_won = True
    elif board[0][2] == O and board[1][1] == O and board[2][0] == O:
        o_won = True

    if x_won:
        return X
    elif o_won:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    empty_count = 0
    for row in board:
        for item in row:
            if item is EMPTY:
                empty_count += 1
    if empty_count == 0:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def sbe(board):
    """
    Returns 0 for non-terminal states for board value.
    """
    return 0