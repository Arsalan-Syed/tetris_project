# heuristic.py

import copy
import numpy as np

def print_board(board):
    height = len(board)
    for h in reversed(range(height)):
        row = " ".join([str(val) for val in board[h]])
        print(row)


defaultWeights = [1.0, 1.0, 5.0, 2.0, 1.0, 1.0, 1.0]


def evaluate(board, weights=defaultWeights, clearedRows=0):
    # Extract height and width and create a board that is more suitable for evaluation
    height = len(board) - 1
    width = len(board[0])
    evalboard = copy.copy(list(reversed(board[0:height])))

    # Extract height of each column
    columnHeight = [0] * width
    # Extract all the holes while we're at it
    holes = 0
    for c in range(width):
        h = height - 1
        while h >= 0:
            if evalboard[h][c] != 0:
                # Set to h + 1 since we convert from zero-index to one-index
                columnHeight[c] = h + 1
                break
            h -= 1
        while h >= 0:
            if evalboard[h][c] == 0:
                holes += 1
            h -= 1

    # Get the max height as well
    maxHeight = max(columnHeight)

    '''
    # Get the largest consecutive row of cells for each row
    rowContinuity = [0]*height
    for h in range(height):
        isRow = False
        consecutiveLength = 0
        for c in range(width):
            if evalboard[h][c] != 0:
                consecutiveLength += 1
            else:
                rowContinuity[h] = max(rowContinuity[h], consecutiveLength)
                consecutiveLength = 0
        rowContinuity[h] = max(rowContinuity[h], consecutiveLength)
    maxContinuity = max(rowContinuity)
    '''
    rowContinuity = [0]
    maxContinuity = 0

    # Holes
    numberOfHoles = holes

    # Bumpiness
    bumpiness = 0
    for c in range(width - 1):
        bumpiness += abs(columnHeight[c] - columnHeight[c+1])

    # Average height
    avgHeight = sum(columnHeight) / width

    # Average continuity
    avgContinuity = 0 #sum(rowContinuity) / maxHeight

    # Full lines
    fullLines = 0 #numberOfFullLines(board)

    # Calculate the heuristic score!
    score = (avgContinuity * weights[0] + maxContinuity * weights[1] + clearedRows * weights[2])
    score -= (numberOfHoles * weights[3] + avgHeight * weights[4] + maxHeight * weights[5] + bumpiness * weights[6])
    return score

'''
If a row is full, each element in the row must be non-zero
'''
def numberOfFullLines(board):
    return len([row for row in board if np.count_nonzero(row) == len(row)])


'''
Returns true if the game state results in a loss
'''
# TODO
def getIsLoss(board):
    return sum(board[0]) > 0


def holes_v1(board, width, maxHeight):
    # Setup a boolean array (maxHeight x width) that says if something is a hole
    # or not
    isHole = [[]]*maxHeight
    for h in range(maxHeight):
        isHole[h] = [False]*width
        for c in range(width):
            if board[h][c] == 0:
                isHole[h][c] = True

    # Simple search for unmarking all the empty spaces that aren't holes
    def unmark_neighbors(iHeight, iWidth, depth):
        # Limit with a depth
        if depth == 0:
            return
        if iWidth > 0:
            if isHole[iHeight][iWidth - 1]:
                isHole[iHeight][iWidth - 1] = False
                unmark_neighbors(iHeight, iWidth - 1, depth - 1)
        if iWidth < (width - 1):
            if isHole[iHeight][iWidth + 1]:
                isHole[iHeight][iWidth + 1] = False
                unmark_neighbors(iHeight, iWidth + 1, depth - 1)
        if iHeight > 0:
            if isHole[iHeight - 1][iWidth]:
                isHole[iHeight - 1][iWidth] = False
                unmark_neighbors(iHeight - 1, iWidth, depth - 1)
        if iHeight < (maxHeight - 1):
            if isHole[iHeight + 1][iWidth]:
                isHole[iHeight + 1][iWidth] = False
                unmark_neighbors(iHeight + 1, iWidth, depth - 1)

    # Now search!
    for c in range(width):
        cHeight = maxHeight
        while board[cHeight - 1][c] == 0:
            if cHeight == 1:
                break
            else:
                cHeight -= 1
        if cHeight != maxHeight:
            cHeight += 1

        if board[cHeight - 1][c] == 0 and isHole[cHeight - 1][c]:
            isHole[cHeight - 1][c] = False
            unmark_neighbors(cHeight - 1, c, 2)

    # Holes
    numberOfHoles = 0
    for h in range(maxHeight):
        numberOfHoles += sum([int(c) for c in isHole[h]])

    return numberOfHoles

def holes_v2(board, width, maxHeight):
    numberOfHoles = 0
    for c in range(width):
        h = maxHeight - 1
        while board[h][c] == 0 and h >= 0:
            h -= 1
        while h >= 0:
            if board[h][c] == 0:
                numberOfHoles += 1
            h -= 1

    return numberOfHoles
