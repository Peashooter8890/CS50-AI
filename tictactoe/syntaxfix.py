import math
import copy

def player(board):
    # get a set of remaining moves (tuples)
    moves = actions(board)

    # if odd number of moves left, X's turn. Else, O's turn.
    if (len(moves) %2 != 0):
        return 'X'
    else:
        return 'O'

def actions(board):
    # Initalize empty set
    moves = set()

    # Load all possible moves into set, then return set
    for row in board:
        for col in row:
            if (board[row,col] == 'EMPTY'):
                moves.add((row,col))
    return moves

def result(board,action):
    # Make deep copy of board
    boardCopy = copy.deepcopy(board)

    # Execute action for current turn player on new board, then return new board
    if player(board) == 'X':
        boardCopy[action[0]][action[1]] = 'X'
        return boardCopy
    else:
        boardCopy[action[0]][action[1]] = 'O'
        return boardCopy

def winChecker(list):
    # Applies custom algorithm to check if winner exists :)

    # If center exists:
    if 'center' in list:
        # If any duplicate items exist, there is a winner
        if len(set(list)) != len(list):
            return True
    else:
        # If both corners and one of either edge exists, there is a winner
        if (all (x in list for x in ['corner1', 'corner2', ('edge1' or 'edge2')]) ):
            return True
    # Every other case has no winner
    return False

def boardFiller(i,j):
# Checks tile location and returns corresponding string

    # If tile is at center:
    if 1 == i == j:
        return 'center'
    
    # If tile is at lower left or upper right corner:
    elif (i == j):
        return 'corner1'

    # If tile is at upper left or lower right corner:
    elif (i + j == 2): 
        return 'corner2'
    
    # if tile is at upper or lower edge:
    elif (j == 1): 
        return 'edge1'

    # if tile is at left or right edge:
    elif (i == 1):
        return 'edge2'

def winner(board):
    # Initialize lists for X and O
    Xlist,Olist = []

    # Calls boardFiller() on each tile other than EMPTY ones
    # boardFiller() returns a string that depends on if tile is edge, center, or corner
    # If tile has X, string appended for Xlist. Vice versa for O
    for row in board:
        for col in row:
            if board[row,col] == 'X':
                Xlist.append(boardFiller(row,col))
            if board[row,col] == 'O':
                Olist.append(boardFiller(row,col))
    
    # Calls algorithm on both lists to determine if winner exists
    if(winChecker(Xlist)):
        return 'X'
    elif (winChecker(Olist)):
        return 'O'
    else:
        return None

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
    if winner(board) == 'X':
        return 1
    if winner(board) == 'O':
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