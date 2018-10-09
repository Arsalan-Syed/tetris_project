"""
Created by Arsalan Syed on 9th October 2018
"""

import copy

from random import randrange as rand


def rotate_clockwise(shape):
    return [[shape[y][x]
             for y in range(len(shape))]
            for x in range(len(shape[0]) - 1, -1, -1)]


def getMaxWidth(piece):
    return max([len(x) for x in piece])


def join_matrixes(mat1, mat2, mat2_off):
    result = copy.deepcopy(mat1)
    off_x, off_y = mat2_off
    for cy, row in enumerate(mat2):
        for cx, val in enumerate(row):
            result[cy + off_y - 1][cx + off_x] += val
    return result


def check_collision(board, shape, offset):
    off_x, off_y = offset
    for cy, row in enumerate(shape):
        for cx, cell in enumerate(row):
            try:
                if cell and board[cy + off_y][cx + off_x]:
                    return True
            except IndexError:
                return True
    return False


class Player(object):

    # TODO
    def play(self, board, nextPiece):
        nextStates = self.getPossibleNextStates(board, nextPiece)
        return nextStates[rand(len(nextStates))]

    '''
    Return all possible board states as a list 
    of 2d arrays
    '''

    def getPossibleNextStates(self, board, nextPiece):
        possibleStates = []

        currentPiece = nextPiece.copy()

        for i in range(4):
            width = getMaxWidth(currentPiece)
            possible_x_placements = 11 - width
            for x in range(possible_x_placements):
                y = 0
                while not check_collision(board, currentPiece, (x, y)):
                    y += 1

                possibleStates.append(join_matrixes(board, currentPiece, (x, y)))

            currentPiece = rotate_clockwise(currentPiece)
        return possibleStates
