#!/usr/bin/python3

import sys

import src.environment as env
import src.filehandler as fh
import src.heuristic as heur


def runInfinitely(weights=heur.defaultWeights):
    useGUI = True
    App = env.TetrisApp(useGUI, weights)
    App.run()


def runSequence(sequenceNumber, useGUI, weights=heur.defaultWeights):
    App = env.TetrisApp(useGUI, weights)
    sequences = fh.loadSequences("sequences/test1.txt")
    print(App.runSequence(sequences[sequenceNumber]))


def main():
    useGUI = True

    print("Choose an option: ")
    print(" 1) run infinitely")
    print(" 2) run sequence 0")
    print(" 3) run sequence 1")
    if sys.version_info > (3, 0):
        choice = input("> ")
    else:
        choice = raw_input("> ")
    choice = choice.strip()
    if choice == "1":
        runInfinitely()
    elif choice == "2":
        runSequence(0,useGUI)
    elif choice == "3":
        runSequence(1,useGUI)
    else:
        print("Invalid option. Input must be either 1, 2 or 3.")


if __name__ == '__main__':
    main()
