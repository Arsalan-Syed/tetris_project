import src.environment as env


def run_random_sequence_GUI():
    App = env.TetrisApp(True)
    App.run()


def run_sequence_0():
    filename = "../sequences/test1.txt"
    sequenceNumber = 0
    App = env.TetrisApp(True)
    App.runSequence(filename, sequenceNumber)



# run_random_sequence_GUI()
