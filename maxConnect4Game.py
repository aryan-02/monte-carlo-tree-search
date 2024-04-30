import ai
import maxConnect4
import argparse

def printGameBoard(board):
    print()
    for i in range(1, maxConnect4.BOARD_COLS + 1):
        print(f"{i:2}", end ='')
    print()
    print("--" * maxConnect4.BOARD_COLS)
    for row in board:
        for item in row:
            if item == 0:
                print(" -", end='')
            else:
                print(f"{item:2}", end='')
        print()
    print()
    p1Score, p2Score = maxConnect4.countScore(board)
    print("Scores:")
    print(f"Player 1: {p1Score:4d},\tPlayer 2: {p2Score:4d}")
    print()

def maxConnect4_interactive(board, rollouts, temp):
    agent = ai.MCTSAgent(ai.Game.MAXCONNECT4, rollouts, temp)
    print("Interactive Max Connect-4.")
    print("Player 1 plays the first move if we start with an empty board.\n")
    player_mark = None
    while player_mark != 1 and player_mark != 2:
        player_mark = int(input("Do you want to play as 1 or 2? "))
    print()
    if player_mark == 1:
        print("You are player 1.\n")
    else:
        print("You are player 2.\n")
    
    if board is None:
        board = maxConnect4.initial_state()
    
    while not maxConnect4.terminal(board):
        printGameBoard(board)
        curr_player = maxConnect4.player(board)
        if curr_player == player_mark:
            print("Enter the column in which you want to put your piece.")
            userMove = int(input("Your Turn: "))
            userMove -= 1
            if maxConnect4.valid_move(board, userMove):
                board = maxConnect4.result(board, userMove)
            else:
                print("Invalid Move. Please Try again.")
        else:
            # computerMove = ai.minimax_decision(ai.Game.MAXCONNECT4, board, depth)
            computerMove = agent.select_move(board)
            print("Computer's turn:", computerMove + 1)
            board = maxConnect4.result(board, computerMove)
    printGameBoard(board)

    print("Game over.")
    winner = maxConnect4.winner(board)
    if winner is None:
        print("It's a tie.")
    elif winner == maxConnect4.player1:
        print("Player 1 won.")
    else:
        print("Player 2 won.")

def oneMove(board, rollouts, temp, output_file_name):
    agent = ai.MCTSAgent(ai.Game.MAXCONNECT4, rollouts, temp)
    if board is None:
        board = maxConnect4.initial_state()
    if maxConnect4.terminal(board):
        print("This is a terminal state.")
        winner = maxConnect4.winner(board)
        if winner is None:
            print("It's a tie.")
        elif winner == maxConnect4.player1:
            print("Player 1 won.")
        else:
            print("Player 2 won.")
    else:
        # move = ai.minimax_decision(ai.Game.MAXCONNECT4, board, depth)
        move = agent.select_move(board)
        curr_player = maxConnect4.player(board)
        print(f"Player {curr_player}'s turn: {move + 1}")
        result_board = maxConnect4.result(board, move)
        printGameBoard(result_board)
        if output_file_name is not None:
            maxConnect4.write_game_file(result_board, output_file_name)

    
def self_play(board, rollouts, temp):
    agent = ai.MCTSAgent(ai.Game.MAXCONNECT4, rollouts, temp)
    if board is None:
        board = maxConnect4.initial_state()
    while not maxConnect4.terminal(board):
        printGameBoard(board)
        # computer_move = ai.minimax_decision(ai.Game.MAXCONNECT4, board, depth)
        computer_move = agent.select_move(board)
        print(computer_move)
        curr_player = maxConnect4.player(board)
        print(f"Player {curr_player}'s turn: {computer_move + 1}")
        board = maxConnect4.result(board, computer_move)
    printGameBoard(board)
    winner = maxConnect4.winner(board)
    if winner is None:
        print("It's a tie.")
    elif winner == maxConnect4.player1:
        print("Player 1 won.")
    else:
        print("Player 2 won.")


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
        board = maxConnect4.read_game_file(args.input)
    except:
        print(f"Could not read input file '{args.input}'. Starting with empty board instead.")
        board = None

if args.mode == "interactive":
    maxConnect4_interactive(board, args.rollouts, args.temp)
elif args.mode == "one-move":
    oneMove(board, args.rollouts, args.temp)
elif args.mode == "self":
    self_play(board, args.rollouts, args.temp)