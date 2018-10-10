"""
Created by Arsalan Syed on 9th October 2018
"""

MIN_VALUE = float("-inf")




'''
Attempts to find a local maximum

Is node a game state or heuristic weights ?
'''


def hill_climb(startNode):
    currentNode = startNode
    maxIterations = 1000
    iter = 0

    while (iter < maxIterations):
        bestEvaluation = MIN_VALUE
        bestNode = None
        for neighbour in get_neighbours(currentNode):
            neighbourEvaluation = evaluation(neighbour)
            if neighbourEvaluation > bestEvaluation:
                bestNode = neighbour
                bestEvaluation = neighbourEvaluation

        if bestEvaluation <= evaluation(currentNode):
            return currentNode

        currentNode = bestNode
