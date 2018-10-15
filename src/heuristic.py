# heuristic.py

import copy
import numpy as np

def print_board(board):
    height = len(board)
    for h in reversed(range(height)):
        row = " ".join([str(val) for val in board[h]])
        print(row)


defaultWeights = [1.0, 4.0, -2.0, -1.0, -1.0, -1.0]


def evaluate(board, weights=defaultWeights, clearedRows=0):
    # Extract height and width and create a board that is more suitable for evaluation
    height = len(board) - 1
    width = len(board[0])
    evalboard = copy.copy(list(reversed(board[0:height])))

    # Extract height of each column
    columnHeight = [0] * width
    # Extract all the holes while we're at it
    numberOfHoles = 0
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
                numberOfHoles += 1
            h -= 1

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
    score += clearedRows * clearedRows * weights[0]
    score += clearedRows * weights[1]
    score += numberOfHoles * weights[2]
    score += avgHeight * weights[3] 
    score += maxHeight * weights[4]
    score += bumpiness * weights[5]
    return score
