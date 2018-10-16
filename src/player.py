"""
Created by Arsalan Syed on 9th October 2018
"""

import src.heuristic as heuristic
from src.helper import *


class Player(object):

    def __init__(self, weights):
        self.weights = weights

    '''
    Simulates the agent making a move. It gets the state of the board and a piece
    and then decides where on the board it will place it.
    
    board: a 2D array representing the board
    currentPiece: (2D array) the piece that we can move at the moment
    nextPiece: (2D array) the piece that will be provided once currentPiece is placed. 
                Default value is -1 (which is not one of the valid pieces from 0 to 6)
    
    returns the new state of the board once currentPiece is placed
    '''

    def play(self, board, pieces, piece_types=None):
        if piece_types is None:
            piece_types = [(max([max(row) for row in p]) - 1) for p in pieces]

        x, y, rot, _ = self.bestMove(board, pieces, piece_types)
        piece = pieces[0]
        for i in range(rot):
            piece = rotate_clockwise(piece)

        return add_piece(board, piece, (x, y))

    '''
    Finds all possible moves and uses the heuristic function to 
    determine the best possible move. 
    
    pieces: list of pieces (we know the current piece and the one after that)
    piece_types: list that indicates what type the elements in pieces are
    '''

    def bestMove(self, board, pieces, piece_types, cleared_rows=0):
        current_piece = pieces[0]
        current_piece_type = piece_types[0]
        new_states = self.getPossibleNextStates(board, current_piece, current_piece_type)

        piece_rotations = [current_piece]
        for i in range(3):
            piece_rotations.append(rotate_clockwise(piece_rotations[-1]))

        best_state = None
        best_evaluation = -100000000

        for new_state in new_states:
            (x, y, rot) = new_state
            add_piece(board, piece_rotations[rot], (x, y))
            board, full_rows = remove_full_rows(board)

            new_cleared_rows = cleared_rows + len(full_rows)

            if len(pieces) > 1:
                _, _, _, value = self.bestMove(board, pieces[1:], piece_types[1:], new_cleared_rows)
            else:
                value = heuristic.evaluate(board, self.weights, new_cleared_rows)

            if value > best_evaluation:
                best_evaluation = value
                best_state = new_state

            board = insert_rows(board, full_rows)
            remove_piece(board, piece_rotations[rot], (x, y))

        x, y, rot = best_state
        return (x, y, rot, best_evaluation)

    '''
    Return all possible board states as a list of 2d arrays
    '''

    def getPossibleNextStates(self, board, current_piece, current_piece_type):
        new_states = []

        numRotations = 4

        if current_piece_type == 6:
            numRotations = 1
        elif current_piece_type in [1, 2, 5]:
            numRotations = 2

        # Get the max height of the current board
        boardHeight = len(board) - 1
        maxHeight = 0
        while maxHeight < boardHeight:
            if sum(board[maxHeight]) != 0:
                break
            maxHeight += 1

        # Each iteration represents a 90 degree rotation
        for rotation in range(numRotations):
            height = len(current_piece)
            width = getMaxWidth(current_piece)
            possible_x_placements = 11 - width

            start_y = max(0, maxHeight - height)

            # For each possible x position, we let the piece fall straight down
            for x in range(possible_x_placements):
                y = start_y
                while not check_collision(board, current_piece, (x, y)):
                    y += 1

                new_states.append((x, y, rotation))

            current_piece = rotate_clockwise(current_piece)

        return new_states
