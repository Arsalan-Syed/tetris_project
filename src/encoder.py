"""
Created by Arsalan Syed on 9th October 2018
"""

PIECE_I = 0
PIECE_O = 1
PIECE_T = 2
PIECE_J = 3
PIECE_L = 4
PIECE_S = 5
PIECE_Z = 6

BOARD_ROWS = 20
BOARD_COLUMNS = 10

'''

'''


def encode(board, nextPiece, gameOver):
    encodedState = ""
    for row in board:
        for element in row:
            encodedState += str(element)

    assert (len(encodedState) == BOARD_COLUMNS * BOARD_ROWS)

    encodedState += "_" + str(nextPiece)

    if gameOver:
        encodedState += "_1"
    else:
        encodedState += "_0"

    return encodedState


# TODO
def decode(encodedState):
    stringSplit = encodedState.split("_")
    return None
