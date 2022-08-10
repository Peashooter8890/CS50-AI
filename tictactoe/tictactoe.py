"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

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

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
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

        if ((matrix[0][i] == 3) or (matrix[1][i] == 3)):
            return X

        if ((matrix[2][i] == 3) or (matrix[3][i] == 3)):
            return O
    
    counter = 0
    for m in matrix:
        for num in m:
            if (counter < 2):
                if (num == 0):
                    conditionX = False
            else:
                if(num == 0):
                    conditionO = False
        counter += 1

    if (conditionX == True):
        for m in matrix:
            print(m)
        return X
    elif (conditionO == True):
        return O
    else:
        return None

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
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
            if board[row][col] == X:
                matrix[0][row]+= 1
                matrix[1][col]+= 1
            if board[row][col] == O:
                matrix[2][row] += 1
                matrix[3][col] += 1
    
    # Calls algorithm on matrix to determine if winner exists
    for b in board:
        print(board)
    return(winChecker(matrix))

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
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
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
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
        v = min(v, MAXVALUE(result(state,action),pruning,condition))

        # If v is smaller than max value, quit iterating
        if (v < pruning):
            print(f"Uh-oh! {v} is less than our maximum node, {pruning}. Protocol exit.")
            return v
    return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
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
    return(MAXVALUE(board,pruning,condition))

[[' ', 'X', 'O'], 
 [' ', 'O', 'X'], 
 ['X', ' ', ' ']]