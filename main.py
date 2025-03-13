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
ai_player = white
player = black

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
        ai_player = white
        player = black
        player_turn = player
        print_board(board)
    elif first_player == 'w':
        print("White player starting...")
        ai_player = black
        player = white
        player_turn = player
    else:
        print("Unexpected value entered")

    while True:
        # human player
        if player_turn == player:
            print("Your turn:")
            row, col = get_player_move(board)
            board[row, col] = player
            print_board(board)
            player_turn = ai_player
        else:
            print("AI's turn:")
            move = minimax(board, 3, ai_player, player, -float('inf'), float('inf'))
            print(f"AI plays: {move}")
            board[move[0], move[1]] = ai_player
            print_board(board)
            player_turn = player

def print_board(board):
    print("   0 1 2 3 4 5 6 7 ")
    for i in range(8):
        temp_string = str(i) + " "
        for j in range(8):
            if board[i,j] == 0:
                temp_string = temp_string + " ."
            elif board[i,j] == black: 
                temp_string = temp_string + " X"
            elif board[i,j] == white: 
                temp_string = temp_string + " O"
        print(temp_string)
    print("\n")

def get_player_move(board):
    # gets move to add to the board
    while True:
        try:
            move = input("Enter your move (row, col): ")
            row, col = map(int, move.split(','))
            if board[row, col] == 0 and is_valid_move(board, row, col, BLACK):
                return row, col
            else:
                print("Invalid move! Try again.")
        except (ValueError, IndexError):
            print("Invalid input! Enter row and column as integers between 0 and 7.")

def is_valid_move(board, row, col, player):
    if board[row, col] != 0:
        return False
    for d in DIRECTIONS:
        x, y = row + d[0], col + d[1]
        found_opponent = False
        while 0 <= x < 8 and 0 <= y < 8 and board[x, y] == -player:
            x += d[0]
            y += d[1]
            found_opponent = True
        if found_opponent and 0 <= x < 8 and 0 <= y < 8 and board[x, y] == player:
            return True
    return False

def evaluate_board(board):
    # Counts number of pieces for each player to keep score
    # add edge spaces
    # corner spaces
    black_count = np.sum(board == black)
    white_count = np.sum(board == white)
    # replace with weighted result based on what we decide are the most important moves
    return black_count - white_count

def minimax(board, depth, ai_player, player, alpha, beta):
    if depth == 0:
        return score_board(board)

    best_move = None
    if player == ai_player:
        max_eval = -float('inf')
        moves = generate_moves(board, ai_player)
        for move in moves:
            new_board = board.copy()
            new_board[move[0], move[1]] = ai_player
            eval = minimax(new_board, depth-1, player, alpha, beta)
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
        moves = generate_moves(board, player)
        for move in moves:
            new_board = board.copy()
            new_board[move[0], move[1]] = player
            eval = minimax(new_board, depth-1, ai_player, alpha, beta)
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
