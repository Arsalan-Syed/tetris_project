"""
Created by Arsalan Syed on 9th October 2018
"""

import src.heuristic as heuristic
from src.helper import *


class Player(object):

    def __init__(self, weights):
        self.weights = weights

    '''
    board: a 2D array representing the board
    currentPiece: the piece that we can move at the moment
    nextPiece: the piece that will be provided once currentPiece is placed
    
    returns the new state of the board once currentPiece is placed
    '''
    def play(self, board, currentPiece, nextPiece=-1):
        nextStates = self.getPossibleNextStates(board, currentPiece)
        scores = [heuristic.evaluate(state, w = self.weights) for state in nextStates]
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