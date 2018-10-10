#!/usr/bin/python3

import src.environment as env

def main():
    App = env.TetrisApp(True)
    App.run()

if __name__ == '__main__':
	main()
