"""
Created by Arsalan Syed on 9th October 2018
"""

import copy
import itertools

from random import randrange as rand
import numpy as np
import environment as env

def normalize(x):
    if x > 0:
        return 1
    else:
        return 0


'''
Higher height is worse
'''


def maxHeight(board):
    height = 0
    while height < len(board):
        if sum(board[height]) > 0:
            break
        height += 1
    return height


def getHeights(board):
    numColumns = len(board[0])

    heights = np.zeros(numColumns)
    for row in board:
        normalizedRow = [normalize(x) for x in row]
        heights = np.add(normalizedRow, heights)

    return heights


'''
Want average height to be as low as possible
'''


def averageHeight(board):
    numRows = len(board)
    heights = getHeights(board)
    return sum(heights) / numRows


def numberOfHoles(board):
    numRows = len(board)
    numColumns = len(board[0])
    numberOfHoles = 0
    for i in range(numRows):
        for j in range(numColumns):
            try:
                top = normalize(board[i][j + 1])
                bottom = normalize(board[i][j - 1])
                left = normalize(board[i - 1][j])
                right = normalize(board[i + 1][j])
            except:
                continue

            if top + bottom + left + right == 4:
                numberOfHoles += 1

    return numberOfHoles


def bumpiness(board):
    heights = getHeights(board)
    differences = []
    for i in range(len(heights) - 1):
        differences.append(np.abs(heights[i + 1] - heights[i]))
    return sum(differences)


'''
All of the heuristic terms should be minimzed,
we want less height,less bumpiness, fewer holes.
So we should maximize -1*heuristicValues
'''


def heuristicValue(board, weights):
    assert (len(weights) == 4)
    heuristicValueVector = [maxHeight(board), averageHeight(board), numberOfHoles(board), bumpiness(board)]
    return np.dot(weights, -1 * heuristicValueVector)


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

'''
Determines how good an AI player is by making it play several games
and counting the average number of rows it clears per game. This will be used
to compare different genetic algorithm (GA) solutions as well as GA's to
other local search algorithms 
'''

# TODO use weights
def player_fitness(weights):
    filename = "../sequences/test1.txt"
    numGames = 3
    score = 0

    for gameNumber in range(numGames):
        App = env.TetrisApp(False)
        score += App.runSequenceNoGUI(filename, gameNumber)

    return score / numGames

def convert(x):
    result = int(x)
    if result == 2:
        return -1
    return result


def getWeightVectorNeighbours(weights,stepSize):
    weightIncrements = []
    chars = "012"
    count = len(weights)
    for item in itertools.product(chars, repeat=count):
        weightIncrements.append([convert(x) for x in item])

    neighbours = []
    for increment in weightIncrements:
        delta = np.multiply(increment, stepSize)
        neighbours.append(np.add(weights, delta))
    return neighbours

# TODO Fitness function should be independent of environment class
def hill_climb(weight_vector):
    stepSize = 0.1
    current_weights = copy.deepcopy(weight_vector)

    while True:
        bestFitness = -10000000
        bestWeights = None
        for neighbour in getWeightVectorNeighbours(current_weights,stepSize):
            neighbourFitness = player_fitness(current_weights)
            if neighbourFitness > bestFitness:
                bestFitness = neighbourFitness
                bestWeights = neighbour

        if bestFitness <= player_fitness(current_weights):
            return current_weights

        current_weights = bestWeights


