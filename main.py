import numpy as np

# Global Vars
black = 1
white = -1
ai_player_color = white
player_color = black
depth_ply = 2   # this is actually 3 somehow
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

    # Find out which player the human player is
    human_player = input("Enter the human player: (Black/White)\n")
    human_player = human_player[0].lower()

    if human_player == 'b':
        print("Human player starting...")
        ai_player_color = white
        player_color = black
        print_board(board)
    elif human_player == 'w':
        print("AI player starting...")
        ai_player_color = black
        player_color = white
        print_board(board)
    else:
        print("Unexpected value entered")
    player_turn = black


    # PLAY THE GAME !!!!
    while True:
        # human player
        if player_turn == player_color:
            print("Your turn:")
            start_x, start_y, row, col = get_player_move(board)
            make_move(board, start_x, start_y, row, col, player_turn)
            print_board(board)
            player_turn = ai_player_color
        else:
            print("AI's turn:")
            move = minimax(board, 2, ai_player_color, player_color, player_turn, -float('inf'), float('inf'))
            print(f"AI plays: {move}")
            start_x, start_y, end_x, end_y, flipped = move
            make_move(board, start_x, start_y, end_x, end_y, player_turn)
            print_board(board)
            player_turn = player_color

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
            start = input("Enter your move start (col, row): ")
            start_x, start_y = map(int, start.split(','))
            move = input("Enter your move (col, row): ")
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

def make_move(board, start_x, start_y, end_x, end_y, player):
    if start_x == end_x and start_y == end_y:  # start and end positions should be different
        return #no valid move
    if board[end_x, end_y] != 0:  # check if the end position is empty
        return
    if start_x == end_x:  # Horizontal move
        board[start_x, min(start_y, end_y):max(start_y, end_y)+1] = player
    elif start_y == end_y:  # Vertical move
        board[min(start_x, end_x):max(start_x, end_x)+1, start_y] = player
    else:  # Diagonal move
        dx = 1 if end_x > start_x else -1
        dy = 1 if end_y > start_y else -1
        for step in range(abs(start_x - end_x) + 1):
            board[start_x + step * dx, start_y + step * dy] = player

def minimax(board, depth, ai_player_color, player_color, player_turn, alpha, beta):
    if depth == 0:   # if depth = 0, end of search, eval board and return
        return evaluate_board(board)

    best_move = None
    if ai_player_color == player_turn:     # We want to max!!
        max_eval = -float('inf')
        #print(ai_player_color)
        moves = generate_moves(board, ai_player_color) # Changed from ai_player to ai_player_color
        if not moves:
            return evaluate_board(board)
        for move in moves:
            start_x, start_y, end_x, end_y, flipped = move
            new_board = board.copy()
            make_move(new_board, start_x, start_y, end_x, end_y, ai_player_color) # Changed from ai_player to ai_player_color
            eval = minimax(new_board, depth-1, ai_player_color, player_color, player_turn*-1, alpha, beta) #swapped player_color and ai_player_color
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        if depth == depth_ply:  ## if at the top and we are done
            return best_move
        return max_eval
    else:                     # we want to min!!!
        min_eval = float('inf')
        #print(player_color)
        moves = generate_moves(board, player_color) # Changed from player to player_color
        if not moves:
            return evaluate_board(board)
        for move in moves:
            start_x, start_y, end_x, end_y, flipped = move
            new_board = board.copy()
            make_move(new_board, start_x, start_y, end_x, end_y, player_color)
            eval = minimax(new_board, depth-1, ai_player_color, player_color, player_turn*-1, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        if depth == depth_ply:
            return best_move
        return min_eval

def direction_search(board, x, y, x_direction, y_direction, player):
    possible_spaces = 0
    move_x = 0
    move_y = 0
    for i, j in zip( range(1, 7-x), range(1, 7-y) ):
        print("checking... ", x+ i*x_direction, y+ j*y_direction)
        if board[ x+ i*x_direction, y+ j*y_direction] == player * -1:
            print("found opposite player")
            possible_spaces = possible_spaces + 1
        elif board[ x+ i*x_direction, y+ j*y_direction] == player:
            print("found me")
            return 0, 0, 0
        elif board[ x+ i*x_direction, y+ j*y_direction] == 0:
            print("found empty space")
            if possible_spaces > 0:
                move_x = x+ i*x_direction
                move_y = y+ j*y_direction
                print("returning possible spaces, move x y", possible_spaces, move_x, move_y)
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
                        #print((i, j, x, y, flipped))
                        moves.append((i, j, x, y, flipped))
    return moves


main()
