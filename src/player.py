"""
Created by Arsalan Syed on 9th October 2018
"""

import src.heuristic as heuristic
from src.helper import *


def remove_duplicate_states(states):
    possible_states = {}
    for state in states:
        possible_states[hash(str(state))] = state

    return list(possible_states.values())

class Player(object):

    def __init__(self, weights):
        self.weights = weights

    '''
    board: a 2D array representing the board
    currentPiece: (2D array) the piece that we can move at the moment
    nextPiece: (2D array) the piece that will be provided once currentPiece is placed. 
                Default value is -1 (which is not one of the valid pieces from 0 to 6)
    
    returns the new state of the board once currentPiece is placed
    '''
    def play(self, board, currentPiece, nextPiece=None):

        bestValue = -10000000
        for neighbour in self.getPossibleNextStates(board, currentPiece):

            # If we know the next piece, we can expand this neighbour in our game tree
            if nextPiece is not None:
                bestNextValue = -10000000
                for nextStateNeighbour in self.getPossibleNextStates(neighbour, nextPiece):
                    value = heuristic.evaluate(nextStateNeighbour, self.weights)
                    if value > bestNextValue:
                        bestNextValue = value

                if bestNextValue > bestValue:
                    bestValue = bestNextValue
                    bestState = neighbour

            # We just evaluate this neighbour
            else:
                value = heuristic.evaluate(neighbour, self.weights)
                if value > bestValue:
                    bestValue = value
                    bestState = neighbour

        return bestState

    '''
    Return all possible board states as a list 
    of 2d arrays
    '''

    def getPossibleNextStates(self, board, current_piece):
        possible_states = []

        current_piece_copy = current_piece.copy()

        # Each iteration represents a 90 degree rotation
        for i in range(4):
            width = getMaxWidth(current_piece_copy)
            possible_x_placements = 11 - width

            # For each possible x position, we let the piece fall straight down
            for x in range(possible_x_placements):
                y = 0
                while not check_collision(board, current_piece_copy, (x, y)):
                    y += 1

                possible_states.append(join_matrixes(board, current_piece_copy, (x, y)))

            current_piece_copy = rotate_clockwise(current_piece_copy)

        return remove_duplicate_states(possible_states)

