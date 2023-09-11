import random

# Constants for game elements
RABBIT = 'r'
RABBIT_WITH_CARROT = 'R'
CARROT = 'c'
RABBIT_HOLE = 'O'
PATHWAY_STONE = '-'

# Initialize the game board
def create_game_board(size, num_carrots, num_holes):
    # Create an empty game board
    board = [[' ' for _ in range(size)] for _ in range(size)]

    # Place rabbit
    rabbit_x, rabbit_y = random.randint(0, size - 1), random.randint(0, size - 1)
    board[rabbit_x][rabbit_y] = RABBIT

    # Place carrots
    for _ in range(num_carrots):
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        while board[x][y] != ' ':
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        board[x][y] = CARROT

    # Place rabbit holes
    for _ in range(num_holes):
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        while board[x][y] != ' ':
            x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        board[x][y] = RABBIT_HOLE

    # Place pathway stones
    for i in range(size):
        for j in range(size):
            if board[i][j] == ' ':
                board[i][j] = random.choice([PATHWAY_STONE, ' '])

    return board, rabbit_x, rabbit_y

# Display the game board
def display_board(board):
    for row in board:
        print(' '.join(row))

# Move the rabbit and handle actions
def move_rabbit(board, rabbit_x, rabbit_y):
    move = input("Enter your move (w/a/s/d/p/j/q to quit): ").lower()

    if move == 'q':
        return False

    new_x, new_y = rabbit_x, rabbit_y

    if move == 'w':
        new_x -= 1
    elif move == 's':
        new_x += 1
    elif move == 'a':
        new_y -= 1
    elif move == 'd':
        new_y += 1

    if move in ('w', 's', 'a', 'd'):
        # Check if the new position is valid
        if 0 <= new_x < len(board) and 0 <= new_y < len(board[0]):
            if board[new_x][new_y] == PATHWAY_STONE:
                print("You cannot move through a stone.")
            elif board[new_x][new_y] == CARROT:
                print("You picked up a carrot!")
                board[new_x][new_y] = ' '
                board[rabbit_x][rabbit_y] = RABBIT_WITH_CARROT
            elif board[new_x][new_y] == RABBIT_HOLE:
                print("You cannot move into a rabbit hole.")
            else:
                board[new_x][new_y] = RABBIT_WITH_CARROT
                board[rabbit_x][rabbit_y] = ' '
                rabbit_x, rabbit_y = new_x, new_y
        else:
            print("Invalid move. Try again.")

    elif move == 'p':
        if board[rabbit_x][rabbit_y] == RABBIT_WITH_CARROT:
            print("You deposited a carrot in a rabbit hole!")
            board[rabbit_x][rabbit_y] = ' '
            # Check if the game is won
            if CARROT not in ''.join([''.join(row) for row in board]):
                print("Congratulations! You collected all the carrots.")
                return False
        else:
            print("You are not holding a carrot.")

    elif move == 'j':
        if board[rabbit_x][rabbit_y] == RABBIT_WITH_CARROT:
            print("You cannot jump with a carrot.")
        else:
            # Check if there is a rabbit hole nearby
            nearby_hole = False
            if rabbit_x > 0 and board[rabbit_x - 1][rabbit_y] == RABBIT_HOLE:
                nearby_hole = True
            elif rabbit_x < len(board) - 1 and board[rabbit_x + 1][rabbit_y] == RABBIT_HOLE:
                nearby_hole = True
            elif rabbit_y > 0 and board[rabbit_x][rabbit_y - 1] == RABBIT_HOLE:
                nearby_hole = True
            elif rabbit_y < len(board[0]) - 1 and board[rabbit_x][rabbit_y + 1] == RABBIT_HOLE:
                nearby_hole = True

            if nearby_hole:
                print("You jumped over a rabbit hole.")
                board[rabbit_x][rabbit_y] = ' '
                # Move to the opposite side of the hole
                if rabbit_x > 0 and board[rabbit_x - 1][rabbit_y] == RABBIT_HOLE:
                    rabbit_x = len(board) - 1
                elif rabbit_x < len(board) - 1 and board[rabbit_x + 1][rabbit_y] == RABBIT_HOLE:
                    rabbit_x = 0
                elif rabbit_y > 0 and board[rabbit_x][rabbit_y - 1] == RABBIT_HOLE:
                    rabbit_y = len(board[0]) - 1
                elif rabbit_y < len(board[0]) - 1 and board[rabbit_x][rabbit_y + 1] == RABBIT_HOLE:
                    rabbit_y = 0
                board[rabbit_x][rabbit_y] = RABBIT

            else:
                print("There are no rabbit holes nearby. You cannot jump.")

    else:
        print("Invalid move. Try again.")

    return True

# Main game loop
def main():
    size = int(input("Enter the size of the game board (minimum 10): "))
    num_carrots = int(input("Enter the number of carrots (at least 2): "))
    num_holes = int(input("Enter the number of rabbit holes (at least 2): "))

    if size < 10 or num_carrots < 2 or num_holes < 2:
        print("Invalid input. Please enter valid values.")
        return

    board, rabbit_x, rabbit_y = create_game_board(size, num_carrots, num_holes)
    carrot_collected = False

    while carrot_collected is False:
        display_board(board)
        carrot_collected = not move_rabbit(board, rabbit_x, rabbit_y)

if __name__ == "__main__":
    main()
