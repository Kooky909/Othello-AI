import numpy as np

# Global Vars
black = 1
white = -1
ai_player = white
player = black
directions = [[0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1,1]]
            #  up  up-right  right down-right down down-left  left  up-left

# Main program
def main():

    # Make board
    board = np.zeros((8, 8))  # 8x8 board with zeros
    board[3, 3] = black
    board[4, 4] = black
    board[3, 4] = white # Opponent piece
    board[4, 3] = white # Opponent piece
    #board[3, 2:6] = -1  # Flip all pieces from column 2 to 5

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
            start_x, start_y, row, col = get_player_move(board)
            make_move(board, start_x, start_y, row, col, player)
            print_board(board)
            player_turn = ai_player
        else:
            print("AI's turn:")
            move = minimax(board, 2, ai_player, player, -float('inf'), float('inf'))
            print(f"AI plays: {move}")
            start_x, start_y, end_x, end_y, flipped = move
            make_move(board, start_x, start_y, end_x, end_y, ai_player)
            print_board(board)
            player_turn = player

# Prints the board
def print_board(board):
    for j in range(7, -1, -1):
        temp_string = str(j) + " "
        for i in range(8):
            if board[i,j] == 0:
                temp_string = temp_string + " ."
            elif board[i,j] == black: 
                temp_string = temp_string + " X"
            elif board[i,j] == white: 
                temp_string = temp_string + " O"
        print(temp_string)
    print("   0 1 2 3 4 5 6 7 ")
    print("\n")

# Gets move to add to the board
def get_player_move(board):
    while True:
        try:
            start = input("Enter your move start (row, col): ")
            start_x, start_y = map(int, start.split(','))
            move = input("Enter your move (row, col): ")
            row, col = map(int, move.split(','))
            if board[row, col] == 0: #and is_valid_move(board, row, col, black):
                return start_x, start_y, row, col
            else:
                print("Invalid move! Try again.")
        except (ValueError, IndexError):
            print("Invalid input! Enter row and column as integers between 0 and 7.")

# Checks move and adds to board
#def is_valid_move(board, row, col, player):
    #if board[row, col] != 0:    # space has to be empty to make a move
       # return False
    #for d in directions:
        #x, y = row + d[0], col + d[1]
       # found_opponent = False
       # while 0 <= x < 8 and 0 <= y < 8 and board[x, y] == -player:
         #   x += d[0]
         #   y += d[1]
         #   found_opponent = True
      #  if found_opponent and 0 <= x < 8 and 0 <= y < 8 and board[x, y] == player:
      #      return True
 #   return False

# Evaluate Function
def evaluate_board(board):
    # Counts number of pieces for each player to keep score
    # add edge spaces
    # corner spaces
    black_count = np.sum(board == black)
    white_count = np.sum(board == white)
    # replace with weighted result based on what we decide are the most important moves
    return black_count - white_count

def make_move(board, start_x, start_y, end_x, end_y, player):    # board[3, 2:6] = -1
    if start_x == end_x:  # Horizontal move
        board[start_x, min(start_y, end_y):max(start_y, end_y)+1] = player
    elif start_y == end_y:  # Vertical move
        board[min(start_x, end_x):max(start_x, end_x)+1, start_y] = player
    else:        # diagonal move
        dx = 1 if end_x > start_x else -1  # Determine row direction (+1 or -1)
        dy = 1 if end_y > start_y else -1  # Determine column direction (+1 or -1)
        for step in range(1, abs(start_x - end_x)):  # Don't include start and end points
            board[start_x + step * dx, start_y + step * dy] = player
    

# AI Minimax algorithm
def minimax(board, depth, ai_player, player, alpha, beta):
    if depth == 0:   # if depth = 0, end of search, eval board and return
        return evaluate_board(board)

    best_move = None
    if player == ai_player:     # We want to max!!
        max_eval = -float('inf')
        moves = generate_moves(board, ai_player)
        for move in moves:
            start_x, start_y, end_x, end_y, flipped = move
            new_board = board.copy()
            make_move(new_board, start_x, start_y, end_x, end_y, ai_player)
            eval = minimax(new_board, depth-1, player, ai_player, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        if depth == 2:  ## if at the top and we are done  
            return best_move
        return max_eval
    else:                     # we want to min!!!
        min_eval = float('inf')
        moves = generate_moves(board, player)
        for move in moves:
            start_x, start_y, end_x, end_y, flipped = move
            new_board = board.copy()
            make_move(new_board, start_x, start_y, end_x, end_y, player)
            eval = minimax(new_board, depth-1, ai_player, player, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        if depth == 2:  
            return best_move
        return min_eval

def direction_search(board, x, y, x_direction, y_direction, player):
    possible_spaces = 0
    move_x = 0
    move_y = 0
    for i, j in zip( range(1, 7-x), range(1, 7-y) ):
        if board[ x+ i*x_direction, y+ j*y_direction] == player * -1:
            possible_spaces = possible_spaces + 1
        elif board[ x+ i*x_direction, y+ j*y_direction] == player:
            return 0, 0, 0
        elif board[ x+ i*x_direction, y+ j*y_direction] == 0:
            if possible_spaces > 0:
                move_x = x+ i*x_direction
                move_y = y+ j*y_direction
                return possible_spaces, move_x, move_y
            else:
                return possible_spaces, move_x, move_y

def generate_moves(board, player):
    # move tuple is (start_x, start_y, end_x, end_y, flipped_pieces)
    moves = []
    for i in range(8):
        for j in range(8):
            if board[i,j] == player:
                for d in directions:
                    flipped, x, y = direction_search(board, i, j, d[0], d[1], player)
                    if flipped != 0:
                        moves.append((i, j, x, y, flipped))
    return moves


main()
