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

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
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
    if(player(board) == X):
        return(MAXVALUE(board,pruning,condition))
    else:
        return(MINVALUE(board,pruning,condition))