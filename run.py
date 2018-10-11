#!/usr/bin/python3

import src.environment as env

def main():
    app = env.TetrisApp(True)
    app.run()

if __name__ == '__main__':
    main()
