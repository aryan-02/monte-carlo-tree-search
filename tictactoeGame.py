import tictactoe
import ai
import argparse


def printBoard(board):
    print("   1  2  3")
    for i, row in enumerate(board):
        print(chr(i + 65), end=' ')
        for item in row:
            if item == tictactoe.EMPTY:
                print(" - ", end='')
            elif item == tictactoe.X:
                print(" X ", end='')
            else:
                print(" O ", end='')
        print()
    print()

def tictactoe_interactive(board, rollouts, temp):
    agent = ai.MCTSAgent(ai.Game.TICTACTOE, rollouts, temp)
    print("Interactive Tic-Tac-Toe\n")
    print("X plays the first move if we start with an empty board.\n")
    player_mark = None
    while player_mark != "X" and player_mark != "O":
        player_mark = input("Do you want to play as X or O? ").upper()
    print()
    if player_mark == "X":
        print("You are X.\n")
    else:
        print("You are O.\n")
    
    if board is None:
        board = tictactoe.initial_state()

    while not tictactoe.terminal(board):
        printBoard(board)
        curr_player = tictactoe.player(board)
        if curr_player == player_mark:
            print("Enter the row and column for your move in the format XY where X can be A, B or C and Y can be 1, 2, or 3.")
            userMoveString = "PQ"
            while len(userMoveString) < 2 or userMoveString[0] not in "ABC" or userMoveString[1] not in "123":
                userMoveString = input("Your turn: ").upper()
            r = ord(userMoveString[0]) - 65
            c = int(userMoveString[1]) - 1
            userMove = (r, c)
            if board[r][c] != tictactoe.EMPTY:
                print("Invalid Move.")
            else:
                board = tictactoe.result(board, userMove)

        else:
            # computer_move = ai.minimax_decision(ai.Game.TICTACTOE,board, depth)
            computer_move = agent.select_move(board)
            r, c = computer_move
            print("Computer's turn: " + chr(65 + r) + str(c + 1))
            board = tictactoe.result(board, computer_move)
    printBoard(board)

    print("Game over.")
    winner = tictactoe.winner(board)
    if winner is None:
        print("It's a tie.")
    elif winner == tictactoe.X:
        print("X won.")
    else:
        print("O won.")

def oneMove(board, rollouts, temp, output_file_name):
    agent = ai.MCTSAgent(ai.Game.TICTACTOE, rollouts, temp)
    if board is None:
        board = tictactoe.initial_state()
    if tictactoe.terminal(board):
        print("This is a terminal state.")
        winner = tictactoe.winner(board)
        if winner is None:
            print("It's a tie.")
        elif winner == tictactoe.X:
            print("X won.")
        else:
            print("O won.")
    else:
        # move = ai.minimax_decision(ai.Game.TICTACTOE ,board, depth)
        move = agent.select_move(board)
        r, c = move
        curr_player = tictactoe.player(board)
        print(f"{curr_player}'s turn: " +  chr(65 + r) + str(c + 1))
        result_board = tictactoe.result(board, move)
        printBoard(result_board)
        if output_file_name is not None:
            tictactoe.write_game_file(result_board, output_file_name)


def self_play(board, rollouts, temp):
    agent = ai.MCTSAgent(ai.Game.TICTACTOE, rollouts, temp)
    if board is None:
        board = tictactoe.initial_state()
    while not tictactoe.terminal(board):
        printBoard(board)
        # computer_move = ai.minimax_decision(ai.Game.TICTACTOE, board, depth)
        computer_move = agent.select_move(board)
        r, c = computer_move
        print(f"{tictactoe.player(board)}'s turn: " + chr(65 + r) + str(c + 1))
        board = tictactoe.result(board, computer_move)
    printBoard(board)
    winner = tictactoe.winner(board)
    if winner is None:
        print("It's a tie.")
    elif winner == tictactoe.X:
        print("X won.")
    else:
        print("O won.")


parser = argparse.ArgumentParser()
parser.add_argument("mode", type=str, choices=['one-move', 'interactive', 'self'], help="Game Mode")
parser.add_argument("-i", "--input", help="Input File to read initial board state (optional). If unspecified, game starts with an empty board.")
parser.add_argument("-o", "--output", help="Output File to write the board state. Only used with one-move mode (optional).")
parser.add_argument("-d", "--rollouts", type=int, default=10000, help="Number of rollouts for MCTS. Defaults to 10000 if unspecified.")
parser.add_argument("-t", "--temp", type=int, default=1.4, help="Temperature for explore/exploit. Defaults to 1.4 if unspecified.")
args = parser.parse_args()

board = None

if args.input:
    print(f"Input file set as '{args.input}'")
    try:
        board = tictactoe.read_game_file(args.input)
    except:
        print(f"Could not read input file '{args.input}'. Starting with empty board instead.")
        board = None

if args.mode == "interactive":
    # print("Depth is", args.depth)
    tictactoe_interactive(board, args.rollouts, args.temp)

elif args.mode == "one-move":
    oneMove(board, args.rollouts, args.temp, args.output)

elif args.mode == "self":
    self_play(board, args.rollouts, args.temp)