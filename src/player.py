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


def add_piece(board, piece, coord):
    off_x, off_y = coord
    for cy, row in enumerate(piece):
        for cx, val in enumerate(row):
            board[cy + off_y - 1][cx + off_x] += val
    return board


def remove_piece(board, piece, coord):
    off_x, off_y = coord
    for cy, row in enumerate(piece):
        for cx, val in enumerate(row):
            board[cy + off_y - 1][cx + off_x] -= val
    return board


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

    def play(self, board, current_piece, current_piece_type):
        new_states = self.getPossibleNextStates(board, current_piece, current_piece_type)

        piece_rotations = [current_piece]
        for i in range(3):
            piece_rotations.append(rotate_clockwise(piece_rotations[-1]))

        best_state = None
        best_evaluation = -100000000

        for new_state in new_states:
            (x, y, rot) = new_state
            add_piece(board, piece_rotations[rot], (x, y))
            value = heuristic.evaluate(board, self.weights)

            if value > best_evaluation:
                best_evaluation = value
                best_state = new_state

            remove_piece(board, piece_rotations[rot], (x, y))

        (x, y, rot) = best_state
        return add_piece(board, piece_rotations[rot], (x, y))

    '''
    Return all possible board states as a list 
    of 2d arrays
    '''

    def getPossibleNextStates(self, board, current_piece, current_piece_type):
        new_states = []

        numRotations = 4

        if current_piece_type == 6:
            numRotations = 1
        elif current_piece_type in [1, 2, 5]:
            numRotations = 2

        # Each iteration represents a 90 degree rotation
        for rotation in range(numRotations):
            width = getMaxWidth(current_piece)
            possible_x_placements = 11 - width

            # For each possible x position, we let the piece fall straight down
            for x in range(possible_x_placements):
                y = 0
                while not check_collision(board, current_piece, (x, y)):
                    y += 1

                new_states.append((x, y, rotation))

            current_piece = rotate_clockwise(current_piece)

        return new_states
