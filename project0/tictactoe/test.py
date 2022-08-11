from doctest import TestResults
from telnetlib import X3PAD
import math, copy, sys, random
X = "X"
O = "O"
EMPTY = "E"

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

def winner(board):
    # Initialize lists for X and O
    Xlist = []
    Olist = []

    # Calls boardFiller() on each tile other than EMPTY ones
    # boardFiller() returns a string that depends on if tile is edge, center, or corner
    # If tile has X, string appended for Xlist. Vice versa for O
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == X:
                Xlist.append(boardFiller(row,col))
            if board[row][col] == O:
                Olist.append(boardFiller(row,col))
    
    # Calls algorithm on both lists to determine if winner exists
    if (easyCaseChecker(Xlist)):
        return X
    elif (easyCaseChecker(Olist)):
        return O
    else:
        for i in range(0,3,2):
            matcherrow = []
            matchercol = []
            for j in range(3):
                matcherrow.append(board[i][j])
                matchercol.append(board[j][i])
            if all(item == matcherrow[0] for item in matcherrow):
                if(matcherrow[0] != EMPTY):
                    return matcherrow[0]
            if all(item == matchercol[0] for item in matchercol):
                if(matchercol[0] != EMPTY):
                    return matchercol[0]
        return None

def boardFiller(i,j):
    # Checks tile location and returns corresponding string

        # If tile is at center:
        if 1 == i == j:
            return 'center'
        
        # If tile is at upper left or lower right corner:
        elif i == j:
            return 'corner1'

        # If tile is at upper right or lower left corner:
        elif i + j == 2: 
            return 'corner2'
        
        # if tile is at upper or lower edge:
        elif j == 1: 
            return 'edge1'

        # if tile is at left or right edge:
        elif i == 1:
            return 'edge2'

def easyCaseChecker(list):
        # Applies custom algorithm to check easy cases :)

        # If center exists:
        if 'center' in list:
            # If any duplicate items exist, there is a winner
            if len(set(list)) != len(list):
                return True
        else:
            return False

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
    mincondition = 0
    # Returns most optimal move
    # state is just a fancy name for board

    # If game is over in simulation, return utility value
    if terminal(state):
        return utility(state)

    # Recursively iterate through every move and assign v the best one
    v = -math.inf
    for action in actions(state):
        v = max(v, MINVALUE(result(state,action),pruning,mincondition))

        # Assign max value to pruning variable
        if (v > pruning):
            tupl = action
            pruning = v
    if (condition == 1):
        return tupl
    else:
        return v
    
def MINVALUE(state,pruning,condition):
    # From this point forward, MAXVALUE() shall not return tuples
    maxcondition = 0

    # state is just the board, but the name "state" is more relevant in MINMAX
    if terminal(state):
        return utility(state)
    
    v = math.inf
    for action in actions(state):
        c_action = min(v, MAXVALUE(result(state,action),pruning,maxcondition))
        if (c_action < v):
            tupl = action
        v = c_action
        # If v is smaller than max value, quit iterating
        if (condition != 1):
            if (v < pruning):
                return v
    if (condition == 1):
        return tupl
    else:
        return v

def minimax(board):
    # If game is over, quit.
    if (terminal(board)):
        return None
    
    # Alpha Beta Pruning - declare variable to keep track of maximum values
    # If any value is less than maximum value, quit search immediately
    pruning = -math.inf

    # We need to receive the tuple that gives us the best move.
    # MAXVALUE() returns v values for recursion. We need a condition variable that will
    # only activate at the end of the first activation of MAXVALUE(). 
    condition = 1

    # Return most optimal move using minimax algorithm
    if(player(board) == X):
        return(MAXVALUE(board,pruning,condition))
    else:
        return(MINVALUE(board,pruning,condition))

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
        same_board = input("Would you like to use only one board for each test? Please type 'y' or 'yes' if so. \n")
        if (same_board.lower() == ('y' or 'yes')):
            testingBoards = []
            testingBoards.append(input("All boards will be the same. Please input board_id for the boards: "))
        else:
            print("All tests will repeat for multiple boards.")
            print("Please input the board_ids for each board that you would like to perform your tests on.")
            testingBoards = []
            while True:
                testingBoard = input("Please enter board_id (or 'quit' if you are done). Enter 'all' to test on all boards.\n")
                if(testingBoard.lower() == 'quit'):
                    break
                if(testingBoard.lower() == 'all'):
                    testingBoards = ['empty', 'random', 'vertical', 'horizontal', 'diagonal']
                    break
                testingBoards.append(testingBoard)

        iteration = input("\nWould you like to iterate each test a different number of times? Please type 'y' or 'yes' if so.\n")
        if (iteration.lower() != ('y' or 'yes')):
            print("Each tests, by themselves, will repeat once.\n")
        else:
            print("Iteration count will be different for each test.\n")

        repeat_id = int(input("How many times would you like to repeat the sequences of your tests? \n"))
        print(f"Your custom test will be repeated {repeat_id} times. \n")
        
        tests = []
        print("Please input the test_id for each tests that you would like to perform.")
        while True:
            test = []
            quitcheck = input("Please input test id (or 'quit' if you are done): ")
            if (quitcheck.lower() == 'quit'):
                print("\n Test input finished. Executing tests... \n")
                break
            test.append(quitcheck)
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
            for testBoard in testingBoards:
                board = boardGenerator(testBoard)
                for test in tests:
                    print(f"Board: {testBoard}")
                    if (test[1] != ("none" or 1)):
                        for i in range(test[1]):
                            print(f"Subtest number {i + 1}")
                            testing(board, test[0])
                            print("\n")
                    else:
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
    
    # Test for winner()
    if (id.lower() == 'winner'):
        print("Initiating test for winner():")
        print(winner(board))

    # Test for minimax()
    if (id.lower() == 'minimax'):
        print("Initiating test for minimax():")
        print(player(board) + "'s turn")
        for b in board:
            print(b)
        print(minimax(board))


# Activate Main() for testing
if __name__ == "__main__":
    main()