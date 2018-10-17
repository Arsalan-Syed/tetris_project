1) Running the program

The program can be run with or without a user interface. Using the interface does make the game run slower but
can be useful for visualising an agent's strategies.

The file run.py is meant for running the game. There are two methods, runInfinitely and runSequence.

a) runInfinitely: runs it on a random sequence until it loses
b) runSequence: runs it on a fixed sequence loaded from a file

Either method can be run using some default weights or by providing custom weights

2) Using pypy

pypy is a faster alternative to running the application in python. It is recommended to use pypy when running
the hill climbing algorithm or the genetic algorithm. For simply letting the agent play the game,
using the default python interpreter is sufficient.




