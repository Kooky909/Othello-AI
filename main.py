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

def main():

    # Make board
    board = np.zeros((8, 8))  # 8x8 board with zeros
    board[3, 3] = 1
    board[4, 4] = 1 
    board[3, 4] = -1 # Opponent piece
    board[4, 3] = -1 # Opponent piece
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

main()
