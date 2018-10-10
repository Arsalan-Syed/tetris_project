"""
Created by Arsalan Syed on 9th October 2018
"""

import src.heuristic as heuristic
from src.helper import *


class Player(object):

    def play(self, board, nextPiece):
        nextStates = self.getPossibleNextStates(board, nextPiece)
        scores = [heuristic.evaluate(state) for state in nextStates]
        return nextStates[scores.index(max(scores))]

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
