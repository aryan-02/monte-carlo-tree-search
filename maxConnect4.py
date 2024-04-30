"""
Max Connect4 Model
"""

import copy

BOARD_ROWS = 6
BOARD_COLS = 7

P1 = 1
P2 = 2
EMPTY = 0

player1 = P1
player2 = P2

def read_game_file(filename):
    """
    Reads a text file and returns the corresponding board array
    """
    with open(filename, 'r') as fh:
        board = []
        for i in range(BOARD_ROWS):
            line = fh.readline().strip()
            board_row = []
            for character in line:
                board_row.append(int(character))
            board.append(board_row)
        return board

def write_game_file(board, filename):
    """
    Outputs the current board configuration to a text file.
    """
    with open(filename, 'w') as fh:
        for row in board:
            for col in row:
                fh.write(str(col))
            fh.write('\n')

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[0 for i in range(BOARD_COLS)] for j in range(BOARD_ROWS)]

def player(board):
    """
    Returns player who has the next turn on a board.
    """
    P1_count = 0
    P2_count = 0
    for row in board:
        for item in row:
            if item == P1:
                P1_count += 1
            elif item == P2:
                P2_count += 1
    return P2 if P1_count > P2_count else P1

def valid_move(board, col):
    # print(f"valid_move {col}: {board[0][col] == 0}")
    return 0 <= col < BOARD_COLS and board[0][col] == 0

def actions(board):
    """
    Returns set of all possible actions available on the board.
    """
    action_set = set()
    for col in range(BOARD_COLS):
        if valid_move(board, col):
            action_set.add(col)
    return action_set

def result(board, action):
    board_copy = copy.deepcopy(board)
    if valid_move(board, action):
        for i in range(5, -1, -1):
            if not board[i][action]:
                board_copy[i][action] = player(board)
                return board_copy
    else:
        raise ValueError("Invalid move.")

def countScore(board):
    player1Score = 0;
    player2Score = 0;

    # Check horizontally
    for row in board:
        # Check player 1
        if row[0:4] == [1]*4:
            player1Score += 1
        if row[1:5] == [1]*4:
            player1Score += 1
        if row[2:6] == [1]*4:
            player1Score += 1
        if row[3:7] == [1]*4:
            player1Score += 1
        # Check player 2
        if row[0:4] == [2]*4:
            player2Score += 1
        if row[1:5] == [2]*4:
            player2Score += 1
        if row[2:6] == [2]*4:
            player2Score += 1
        if row[3:7] == [2]*4:
            player2Score += 1

    # Check vertically
    for j in range(7):
        # Check player 1
        if (board[0][j] == 1 and board[1][j] == 1 and
                board[2][j] == 1 and board[3][j] == 1):
            player1Score += 1
        if (board[1][j] == 1 and board[2][j] == 1 and
                board[3][j] == 1 and board[4][j] == 1):
            player1Score += 1
        if (board[2][j] == 1 and board[3][j] == 1 and
                board[4][j] == 1 and board[5][j] == 1):
            player1Score += 1
        # Check player 2
        if (board[0][j] == 2 and board[1][j] == 2 and
                board[2][j] == 2 and board[3][j] == 2):
            player2Score += 1
        if (board[1][j] == 2 and board[2][j] == 2 and
                board[3][j] == 2 and board[4][j] == 2):
            player2Score += 1
        if (board[2][j] == 2 and board[3][j] == 2 and
                board[4][j] == 2 and board[5][j] == 2):
            player2Score += 1

    # Check diagonally

    # Check player 1
    if (board[2][0] == 1 and board[3][1] == 1 and
            board[4][2] == 1 and board[5][3] == 1):
        player1Score += 1
    if (board[1][0] == 1 and board[2][1] == 1 and
            board[3][2] == 1 and board[4][3] == 1):
        player1Score += 1
    if (board[2][1] == 1 and board[3][2] == 1 and
            board[4][3] == 1 and board[5][4] == 1):
        player1Score += 1
    if (board[0][0] == 1 and board[1][1] == 1 and
            board[2][2] == 1 and board[3][3] == 1):
        player1Score += 1
    if (board[1][1] == 1 and board[2][2] == 1 and
            board[3][3] == 1 and board[4][4] == 1):
        player1Score += 1
    if (board[2][2] == 1 and board[3][3] == 1 and
            board[4][4] == 1 and board[5][5] == 1):
        player1Score += 1
    if (board[0][1] == 1 and board[1][2] == 1 and
            board[2][3] == 1 and board[3][4] == 1):
        player1Score += 1
    if (board[1][2] == 1 and board[2][3] == 1 and
            board[3][4] == 1 and board[4][5] == 1):
        player1Score += 1
    if (board[2][3] == 1 and board[3][4] == 1 and
            board[4][5] == 1 and board[5][6] == 1):
        player1Score += 1
    if (board[0][2] == 1 and board[1][3] == 1 and
            board[2][4] == 1 and board[3][5] == 1):
        player1Score += 1
    if (board[1][3] == 1 and board[2][4] == 1 and
            board[3][5] == 1 and board[4][6] == 1):
        player1Score += 1
    if (board[0][3] == 1 and board[1][4] == 1 and
            board[2][5] == 1 and board[3][6] == 1):
        player1Score += 1

    if (board[0][3] == 1 and board[1][2] == 1 and
            board[2][1] == 1 and board[3][0] == 1):
        player1Score += 1
    if (board[0][4] == 1 and board[1][3] == 1 and
            board[2][2] == 1 and board[3][1] == 1):
        player1Score += 1
    if (board[1][3] == 1 and board[2][2] == 1 and
            board[3][1] == 1 and board[4][0] == 1):
        player1Score += 1
    if (board[0][5] == 1 and board[1][4] == 1 and
            board[2][3] == 1 and board[3][2] == 1):
        player1Score += 1
    if (board[1][4] == 1 and board[2][3] == 1 and
            board[3][2] == 1 and board[4][1] == 1):
        player1Score += 1
    if (board[2][3] == 1 and board[3][2] == 1 and
            board[4][1] == 1 and board[5][0] == 1):
        player1Score += 1
    if (board[0][6] == 1 and board[1][5] == 1 and
            board[2][4] == 1 and board[3][3] == 1):
        player1Score += 1
    if (board[1][5] == 1 and board[2][4] == 1 and
            board[3][3] == 1 and board[4][2] == 1):
        player1Score += 1
    if (board[2][4] == 1 and board[3][3] == 1 and
            board[4][2] == 1 and board[5][1] == 1):
        player1Score += 1
    if (board[1][6] == 1 and board[2][5] == 1 and
            board[3][4] == 1 and board[4][3] == 1):
        player1Score += 1
    if (board[2][5] == 1 and board[3][4] == 1 and
            board[4][3] == 1 and board[5][2] == 1):
        player1Score += 1
    if (board[2][6] == 1 and board[3][5] == 1 and
            board[4][4] == 1 and board[5][3] == 1):
        player1Score += 1

    # Check player 2
    if (board[2][0] == 2 and board[3][1] == 2 and
            board[4][2] == 2 and board[5][3] == 2):
        player2Score += 1
    if (board[1][0] == 2 and board[2][1] == 2 and
            board[3][2] == 2 and board[4][3] == 2):
        player2Score += 1
    if (board[2][1] == 2 and board[3][2] == 2 and
            board[4][3] == 2 and board[5][4] == 2):
        player2Score += 1
    if (board[0][0] == 2 and board[1][1] == 2 and
            board[2][2] == 2 and board[3][3] == 2):
        player2Score += 1
    if (board[1][1] == 2 and board[2][2] == 2 and
            board[3][3] == 2 and board[4][4] == 2):
        player2Score += 1
    if (board[2][2] == 2 and board[3][3] == 2 and
            board[4][4] == 2 and board[5][5] == 2):
        player2Score += 1
    if (board[0][1] == 2 and board[1][2] == 2 and
            board[2][3] == 2 and board[3][4] == 2):
        player2Score += 1
    if (board[1][2] == 2 and board[2][3] == 2 and
            board[3][4] == 2 and board[4][5] == 2):
        player2Score += 1
    if (board[2][3] == 2 and board[3][4] == 2 and
            board[4][5] == 2 and board[5][6] == 2):
        player2Score += 1
    if (board[0][2] == 2 and board[1][3] == 2 and
            board[2][4] == 2 and board[3][5] == 2):
        player2Score += 1
    if (board[1][3] == 2 and board[2][4] == 2 and
            board[3][5] == 2 and board[4][6] == 2):
        player2Score += 1
    if (board[0][3] == 2 and board[1][4] == 2 and
            board[2][5] == 2 and board[3][6] == 2):
        player2Score += 1

    if (board[0][3] == 2 and board[1][2] == 2 and
            board[2][1] == 2 and board[3][0] == 2):
        player2Score += 1
    if (board[0][4] == 2 and board[1][3] == 2 and
            board[2][2] == 2 and board[3][1] == 2):
        player2Score += 1
    if (board[1][3] == 2 and board[2][2] == 2 and
            board[3][1] == 2 and board[4][0] == 2):
        player2Score += 1
    if (board[0][5] == 2 and board[1][4] == 2 and
            board[2][3] == 2 and board[3][2] == 2):
        player2Score += 1
    if (board[1][4] == 2 and board[2][3] == 2 and
            board[3][2] == 2 and board[4][1] == 2):
        player2Score += 1
    if (board[2][3] == 2 and board[3][2] == 2 and
            board[4][1] == 2 and board[5][0] == 2):
        player2Score += 1
    if (board[0][6] == 2 and board[1][5] == 2 and
            board[2][4] == 2 and board[3][3] == 2):
        player2Score += 1
    if (board[1][5] == 2 and board[2][4] == 2 and
            board[3][3] == 2 and board[4][2] == 2):
        player2Score += 1
    if (board[2][4] == 2 and board[3][3] == 2 and
            board[4][2] == 2 and board[5][1] == 2):
        player2Score += 1
    if (board[1][6] == 2 and board[2][5] == 2 and
            board[3][4] == 2 and board[4][3] == 2):
        player2Score += 1
    if (board[2][5] == 2 and board[3][4] == 2 and
            board[4][3] == 2 and board[5][2] == 2):
        player2Score += 1
    if (board[2][6] == 2 and board[3][5] == 2 and
            board[4][4] == 2 and board[5][3] == 2):
        player2Score += 1
    
    return player1Score, player2Score

def winner(board):
    p1_score, p2_score = countScore(board)
    if p1_score > p2_score:
        return P1
    elif p2_score > p1_score:
        return P2
    else:
        return None

# Uncomment the two lines to change it to regular connect4.
def terminal(board):
    emptyCells = sum(board[row].count(0) for row in range(BOARD_ROWS))
    x, y = countScore(board)
    return emptyCells == 0  or x != y

def utility(board):
    """
    Returns Infinity if Player 1 has won the game, -Infinity if Player 2 has won, 0 otherwise.
    """
    if winner(board) == P1:
        return float('inf')
    elif winner(board) == P2:
        return -float('inf')
    else:
        return 0

def sbe(board):
    """
    Static board evaluation function for when Minimax depth limit is reached.
    """
    P1_score, P2_score = countScore(board)
    return P1_score - P2_score

