import numpy as np

# Global Vars
black = 1
white = -1
ai_player_color = white
player_color = black
depth_ply = 5
directions = [[0,1], [1,1], [1,0], [1,-1], [0,-1], [-1,-1], [-1,0], [-1,1]]
            #  up  up-right  right down-right down down-left  left  up-left
board_stack = []

# Main program
def main():
    global ai_player_color, player_color

    board = np.zeros((8, 8))  # Make board and set original pieces
    board[3, 3] = black
    board[4, 4] = black
    board[3, 4] = white
    board[4, 3] = white

    human_player = input("Enter the human player: (Black[X] as 'b' /White[O] as 'w')\n")
    if human_player == 'b':
        ai_player_color = white
        player_color = black
    elif human_player == 'w':
        ai_player_color = black
        player_color = white
    else:
        print("Unexpected value entered")
        return

    player_turn = black
    print_board(board)
    print_piece_counts(board)
    moves_player = []
    moves_ai = []

    while True:
        if player_turn == player_color:
            print("Your turn:")
            moves_player = generate_moves(board, player_color)
            if not moves_player:
                print("No moves available, skipping turn...")
                player_turn = ai_player_color
            else:
                new_board = board.copy()
                board_stack.append(new_board)
                row, col, board = get_player_move(board, player_color)
                make_move(board, row, col, player_color)
                print_board(board)
                print_piece_counts(board)
                player_turn = ai_player_color
        else:
            print("AI's turn:")
            moves_ai = generate_moves(board, ai_player_color)
            if not moves_ai:
                print("No moves available, skipping turn...")
                player_turn = player_color
            else:
                move = minimax(board, depth_ply, ai_player_color, player_color, player_turn, -float('inf'), float('inf'))
                row, col, _ = move
                print(f"AI plays at ({row}, {col})")
                make_move(board, row, col, ai_player_color)
                print_board(board)
                print_piece_counts(board)
                player_turn = player_color

        # End game logic
        black_count, white_count = count_pieces(board)
        if black_count == 0 or white_count == 0 or black_count + white_count == 64 or (not moves_ai and not moves_player):
            print("Game Over!")
            winner = "Black" if black_count > white_count else "White"
            print(f"{winner} wins!")
            break

# Print the board
def print_board(board):
    for j in range(7, -1, -1):
        temp_string = str(j) + " "
        for i in range(8):
            if board[i, j] == 0:
                temp_string += " ."
            elif board[i, j] == black:
                temp_string += " X"
            else:
                temp_string += " O"
        print(temp_string)
    print("   0 1 2 3 4 5 6 7\n")

def print_piece_counts(board):
    black_count, white_count = count_pieces(board)
    print(f"Black pieces: {black_count}, White pieces: {white_count}\n")

def count_pieces(board):
    black_count = np.sum(board == black)
    white_count = np.sum(board == white)
    return black_count, white_count

# Gets move to add to the board
def get_player_move(board, player):
    while True:
        try:
            move = input("Enter your move -- include comma (col, row): ")
            if move == "undo":
                board = undo_move()
                print_board(board)
                move = input("Enter your move -- include comma (col, row): ")
            x, y = map(int, move.split(','))
            if board[x, y] == 0:
                valid = False
                for d in directions:
                    if can_flip(board, x, y, d[0], d[1], player):
                        valid = True
                        break
                if valid:
                    return x, y, board
            print("Invalid move, try again.")
        except (ValueError, IndexError):
            print("Invalid input, enter row and column as integers between 0 and 7.")

def make_move(board, x, y, player):
    board[x, y] = player
    for d in directions:
        if can_flip(board, x, y, d[0], d[1], player):
            flip_pieces(board, x, y, d[0], d[1], player)

def undo_move():
    board_stack.pop()
    new_board = board_stack[-1]
    print("Returning to last human player move...")
    return new_board

# Sees if there are player pieces in a given direction
def can_flip(board, x, y, dx, dy, player):
    x += dx
    y += dy
    count = 0
    while 0 <= x < 8 and 0 <= y < 8:
        if board[x, y] == -player:
            count += 1
        elif board[x, y] == player:
            return count > 0
        else:
            break
        x += dx
        y += dy
    return False

# Switches all player pieces as needed for a move
def flip_pieces(board, x, y, dx, dy, player):
    x += dx
    y += dy
    while 0 <= x < 8 and 0 <= y < 8 and board[x, y] == -player:
        board[x, y] = player
        x += dx
        y += dy

def evaluate_board(board):
    score = 0
    opponent = -ai_player_color
    corners = [(0,0), (0,7), (7,0), (7,7)]
    edges = [(i, j) for i in range(8) for j in range(8) if (i in [0,7] or j in [0,7]) and (i, j) not in corners]

    player_corners = sum(board[x,y] == ai_player_color for x,y in corners)
    player_edges = sum(board[x,y] == ai_player_color for x,y in edges)
    player_other = np.sum(board == ai_player_color) - player_corners - player_edges

    opponent_total = np.sum(board == opponent)

    score = (player_other * 1) + (player_edges * 1.5) + (player_corners * 2) - opponent_total
    return score

def minimax(board, depth, ai_color, human_color, player_turn, alpha, beta):
    if depth == 0:
        return evaluate_board(board)

    best_move = None
    moves = generate_moves(board, player_turn)
    if not moves:
        return evaluate_board(board)

    if player_turn == ai_color:
        max_eval = -float('inf')
        for move in moves:
            x, y, _ = move
            new_board = board.copy()
            make_move(new_board, x, y, player_turn)
            eval = minimax(new_board, depth - 1, ai_color, human_color, -player_turn, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return best_move if depth == depth_ply else max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            x, y, _ = move
            new_board = board.copy()
            make_move(new_board, x, y, player_turn)
            eval = minimax(new_board, depth - 1, ai_color, human_color, -player_turn, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return best_move if depth == depth_ply else min_eval

# evaluates moves based on number of flips
# still needed for evaluate_moves
def direction_search(board, x, y, dx, dy, player):
    flips = 0
    i, j = x + dx, y + dy
    while 0 <= i < 8 and 0 <= j < 8:
        if board[i, j] == -player:
            flips += 1
        elif board[i, j] == player:
            #return flips, x, y
            return flips
        else:
            break
        i += dx
        j += dy
    #return 0, x, y
    return 0

def generate_moves(board, player):
    moves = []
    for i in range(8):
        for j in range(8):
            if board[i, j] == 0:
                total_flips = 0
                for d in directions:
                    #flips, _, _ = direction_search(board, i, j, d[0], d[1], player)
                    flips = direction_search(board, i, j, d[0], d[1], player)
                    total_flips += flips
                if total_flips > 0:
                    #moves.append((None, None, i, j, total_flips))
                    moves.append((i, j, total_flips))
    return moves

main()
