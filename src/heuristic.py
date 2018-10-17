# heuristic.py

def print_board(board):
    height = len(board)
    for h in reversed(range(height)):
        row = " ".join([str(val) for val in board[h]])
        print(row)


# Chosen by us:
defaultWeights = [5.0, -2.0, -1.0, -1.0, -1.0]
# Genetic Algorithm result:
#defaultWeights = [-13.88, -13.12, -9.18, -3.21, -2.0]
# Hill Climb result:
#defaultWeights = [4.15, -2.4, -0.75, -0.4, -0.4]

'''
Calculates the heuristic value of the board
'''
def evaluate(board, weights=defaultWeights, clearedRows=0, maxHeight=0):
    # Extract height and width and create a board that is more suitable for evaluation
    height = len(board) - 1
    width = len(board[0])

    # Extract height of each column
    columnHeight = [0] * width
    # Extract all the holes while we're at it
    numberOfHoles = 0
    for c in range(width):
        h = maxHeight
        while h < height:
            if board[h][c] != 0:
                columnHeight[c] = height - h
                break
            h += 1
        while h < height:
            if board[h][c] == 0:
                numberOfHoles += 1
            h += 1

    # Get the max height as well
    maxHeight = max(columnHeight)

    # Bumpiness
    bumpiness = 0
    for c in range(width - 1):
        bumpiness += abs(columnHeight[c] - columnHeight[c+1])

    # Average height
    avgHeight = sum(columnHeight) / width

    # Calculate the heuristic score!
    score = 0
    score += clearedRows * weights[0]
    score += numberOfHoles * weights[1]
    score += avgHeight * weights[2]
    score += maxHeight * weights[3]
    score += bumpiness * weights[4]
    return score
