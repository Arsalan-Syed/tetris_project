#!/usr/bin/python3

import src.environment as env
import src.filehandler as fh
import src.heuristic as heur


def runInfinitely(weights=heur.defaultWeights):
    useGUI = True
    App = env.TetrisApp(useGUI,weights)
    App.run()


def runSequence(sequenceNumber, useGUI, weights=heur.defaultWeights):
    App = env.TetrisApp(useGUI, weights)
    sequences = fh.loadSequences("sequences/test1.txt")
    print(App.runSequence(sequenceNumber))


def main():
    useGUI = True

    # runInfinitely()
    # runSequence(0,useGUI)
    # runSequence(1,useGUI)


if __name__ == '__main__':
    main()
