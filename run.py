#!/usr/bin/python3

import src.environment as env
import src.filehandler as fh

def main():
    random = False
    App = env.TetrisApp(True)

    if random:
        App.run()
    else:
        sequences = fh.loadSequences("sequences/test1.txt")
        App.runSequence(sequences[0])

if __name__ == '__main__':
	main()
