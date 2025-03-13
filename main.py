#####
## Okaaayyyyyy
####

import numpy as np

#board class
#    struct
#    make board
#    copy board
#    change board?
#    print board

#receive input from user
#- check move to see if its possible or assume playing optimally

#option for black first or white first

#player makes move::::
#computer assesses next possible moves (depth 1)
#computer assess which is best using evaluation function 
#computer makes that move

#dept > 1
#computer assesses next possible moves recursively???? DFS or BFS?? no way BFS right
#computer assess which is best using evaluation function 
#computer makes that move

black = 1
white = -1

def main():

    # Make board
    board = np.zeros((8, 8))  # 8x8 board with zeros
    board[3, 3] = black
    board[4, 4] = black
    board[3, 4] = white # Opponent piece
    board[4, 3] = white # Opponent piece
    #board[3, 2:6] *= -1  # Flip all pieces from column 2 to 5


    # are we playing against the AI??????

    # Find out which play is playing first - set to black for testing
    #first_player = input("Enter the player to start: (Black/White)\n")
    #first_player = first_player[0].lower()
    first_player = 'b'

    if first_player == 'b':
        print("Black player starting...")
        print_board(board)
    elif first_player == 'w':
        print("White player starting...")
    else:
        print("Unexpected value entered")

def print_board(board):
    print("   0 1 2 3 4 5 6 7 ")
    for i in range(8):
        temp_string = str(i) + " "
        for j in range(8):
            if board[i,j] == 0:
                temp_string = temp_string + " ."
            elif board[i,j] == 1: 
                temp_string = temp_string + " X"
            elif board[i,j] == -1: 
                temp_string = temp_string + " O"
        print(temp_string)
    print("\n")

def evaluate_board(board):
    # Counts number of pieces for each player to keep score
    black_count = np.sum(board == BLACK)
    white_count = np.sum(board == WHITE)
    return black_count - white_count

def minimax(board, depth, player, alpha, beta):
    if depth == 0:
        return evaluate_board(board)

    best_move = None
    if player == white:
        max_eval = -float('inf')
        moves = generate_moves(board, white)
        for move in moves:
            new_board = board.copy()
            new_board[move[0], move[1]] = white
            eval = minimax(new_board, depth-1, black, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        if depth == 3:  
            return best_move
        return max_eval
    else:
        min_eval = float('inf')
        moves = generate_moves(board, black)
        for move in moves:
            new_board = board.copy()
            new_board[move[0], move[1]] = black
            eval = minimax(new_board, depth-1, white, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        if depth == 3:  
            return best_move
        return min_eval


main()
