from doctest import TestResults
from telnetlib import X3PAD
import math, copy, sys, random
X = "X"
O = "O"
EMPTY = " "

def player(board):
    # get a set of remaining moves (tuples)
    moves = actions(board)

    # if odd number of moves left, X's turn. Else, O's turn.
    if (len(moves) %2 != 0):
        return X
    else:
        return O

def actions(board):
    # Initalize empty set
    moves = set()

    # Load all possible moves into set, then return set
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (board[i][j] == EMPTY):
                moves.add((i,j))
    return moves

def result(board,action):
    # Make deep copy of board
    boardCopy = copy.deepcopy(board)

    # Execute action for current turn player on new board, then return new board
    if player(board) == X:
        boardCopy[action[0]][action[1]] = X
        return boardCopy
    else:
        boardCopy[action[0]][action[1]] = O
        return boardCopy

def winChecker(matrix):
    # Applies custom algorithm to check if winner exists :)
    conditionX = True
    conditionO = True
    for i in range(len(matrix[0])):
        if (matrix[0][i] or matrix[1][i] == 3):
            return X
        if (matrix[2][i] or matrix[3][i] == 3):
            return O
        if (matrix[0][i] and matrix[1][i] != 1):
            conditionX = False
        if (matrix[2][i] or matrix[3][i] != 1):
            conditionO = False
    if (conditionX == True):
        return X
    elif (conditionO == True):
        return O
    else:
        return None

def winner(board):
    # Initialize 4x3 matrix for col and row for both X and O
    matrix = [
        [0,0,0], # row for X
        [0,0,0], # col for X
        [0,0,0], # row for O
        [0,0,0] # col for O
    ]

    # For each tile, append to matrix.
    for row in range(len(board)):
        for col in range(len(board[0])):
            if col == X:
                matrix[0][row]+= 1
                matrix[1][col]+= 1
            if col == O:
                matrix[2][row] += 1
                matrix[3][col] += 1
    
    # Calls algorithm on matrix to determine if winner exists
    return(winChecker(matrix))

def terminal(board):
    # Store set of moves (tuples)
    moves = actions(board)

    # If there are no moves in the set, game is over.
    if len(moves) == 0:
        return True
    
    # If someone won the game, game is over.
    if (winner(board) != None):
        return True

    # Else, game is not over.
    return False
    
def utility(board):
    # If X won, return 1. If draw, return 0. If O won, return -1.
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0
    
def MAXVALUE(state,pruning,condition):
    # Returns most optimal move
    # state is just a fancy name for board

    # If game is over in simulation, return utility value
    if terminal(state):
        return utility(state)

    # Recursively iterate through every move and assign v the best one
    v = -math.inf
    for action in actions(state):
        v = max(v, MINVALUE(result(state,action),pruning))

        # Assign max value to pruning variable
        if (v > pruning):
            tupl = action
            pruning = v
    if (condition == 1):
        return tupl
    else:
        return v
    
def MINVALUE(state,pruning):
    # From this point forward, MAXVALUE() shall not return tuples
    condition = 0

    # state is just the board, but the name "state" is more relevant in MINMAX
    if terminal(state):
        return utility(state)
    
    v = math.inf
    for action in actions(state):
        v = min(v, MAXVALUE(result(state,action)),pruning)

        # If v is smaller than max value, quit iterating
        if (v < pruning):
            print(f"Uh-oh! {v} is less than our maximum node, {pruning}. Protocol exit.")
            return v
    return v

def randomBoard(board):
    for i in range(len(board)):
            for j in range(len(board[i])):
                board[i][j] = random.choice([X,O,EMPTY])
    return board

def boardGenerator(board_id):
    player = random.choice([X,O])
    number = random.choice([0,1,2])
    boolean = random.choice([0,1])
    board = [[EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY],
             [EMPTY, EMPTY, EMPTY]]

    # Return empty board
    if (board_id == 'empty'):
        return board
    
    # Return random board
    elif (board_id == 'random'):
        randomBoard(board)

    # Return vertical win, randomly choose X or O for the win
    elif (board_id == 'vertical'):
        randomBoard(board)
        for i in range(len(board)):
            board[number][i] = player
    
    # Return horizontal win, randomly choose X or O for the win
    elif (board_id == 'horizontal'):
        randomBoard(board)
        for i in range(len(board)):
            board[i][number] = player
    
    # Return diagonal win, randomly choose X or O for the win
    elif (board_id == 'diagonal'):
        randomBoard(board)
        if (boolean == 0):
            for i in range(len(board)):
                board[i][i] = player
        else:
            for i in range(len(board)):
                board[2-i][0+i] = player

    # Return generated board
    return board

def main():
    # Get test id
    id = None
    try:
        id = sys.argv[1]
        print(id)
    except:
        print("Please enter test id as command line argument.", end = "")
        quit

    if (id.lower() == 'custom'):
        print("Welcome to custom testing services.\n")
        print("Invalid inputs will cause an error later, so please be sure to type the correct inputs. \n")
        same_board = input("Would you like to use the same board for each test? Please type 'y' or 'yes' if so. \n")
        if (same_board.lower() == ('y' or 'yes')):
            board_id = input("\nAll boards will be the same. Please input board_id for the boards: ")
            board = boardGenerator(board_id)
        else:
            print("\nBoard_id will be different for each test.")
        iteration = input("Would you like to iterate each test a different number of times? Please type 'y' or 'yes' if so. \n")
        if (iteration.lower() == ('y' or 'yes')):
            print("\nEach tests, by themselves, will repeat once.")
        else:
            print("\nIteration count will be different for each test.")
        repeat_id = int(input("How many times would you like to repeat the sequences of your tests? \n"))
        print(f"Your custom test will be repeated {repeat_id} times. \n")
        
        tests = []
        print("Please input the test_id for each tests that you would like to perform. ")
        while True:
            test = []
            quitcheck = input("Please input test id (or 'quit' if you are done): ")
            if (quitcheck.lower() == 'quit'):
                print("\n Test input finished. Executing tests... \n")
                break
            test.append(quitcheck)
            if (same_board.lower() != ('y' or 'yes')):
                print(same_board)
                test.append(input("\nPlease input board id for your test: "))
            else:
                test.append("none")
            if (iteration.lower() == ('y' or 'yes')):
                test.append(int(input("\nPlease input iteration count for your test: ")))
            else:
                test.append("none")
            tests.append(test)
        
        for repeat in range(repeat_id):
            if (repeat_id > 1):
                print("--------------------------------------")
                print("\n")
                print(f"CUSTOM TEST SEQUENCE {repeat + 1}")
                print("\n")
            for test in tests:
                if (test[2] != ("none" or 1)):
                    for i in range(test[2]):
                        print(f"Subtest number {i + 1}")
                        if (same_board.lower() == ('y' or 'yes')):
                            testing(board, test[0])
                        else:
                            board = boardGenerator(test[1])
                            testing(board, test[0])
                        print("\n")
                else:
                    if (same_board.lower() == ('y' or 'yes')):
                        testing(board, test[0])
                    else:
                        board = boardGenerator(test[1])
                        testing(board, test[0])
                    print("\n")
    else:
        try:
            board_id = sys.argv[2]
        except:
            board_id = 0
        try:
            repeat_id = int(sys.argv[3])
        except:
            repeat_id = 1

        for repeat in range(repeat_id):
            print("\n")
            if (repeat_id > 1):
                print(f"TEST NUMBER {repeat + 1}")
            board = boardGenerator(board_id)
            testing(board,id)
        print("\n")

def testing(board,id):
    # Test for board
    if (id.lower() == 'board'):
        print("Initiating test for board()")
        for i in range(len(board)):
            print(board[i])

    # Test for actions()
    if (id.lower() == 'actions'):
        print("Initiating test for actions():")
        print(str(len(actions(board))) + " moves availiable.")
        print(actions(board))

    # Test for player()
    if (id.lower() == 'player'):
        print("Initiating test for player():")
        print(player(board))

    # Test for result()
    if (id.lower() == 'result'):
        act1 = random.choice([0,1,2])
        act2 = random.choice([0,1,2])
        action = (act1,act2)
        print("Initiating test for result():")
        board = result(board,action)
        for i in range(len(board)):
            print(board[i])
    
    if (id.lower() == 'winner'):
        print("Initiating test for winner():")
        print(winner(board))
        


# Activate Main() for testing
if __name__ == "__main__":
    main()