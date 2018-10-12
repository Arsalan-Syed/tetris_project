#!/usr/bin/python3

import src.environment as env
import src.filehandler as fh

def main():
    random = False
    useGUI = True

    App = env.TetrisApp(useGUI)

    if random:
        App.run()
    else:
        sequences = fh.loadSequences("sequences/test2.txt")
        print(App.runSequence(sequences[0]))


if __name__ == '__main__':
    main()
