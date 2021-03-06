#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Very simple tetris implementation
#
# Control keys:
# Down - Drop stone faster
# Left/Right - Move stone
# Up - Rotate Stone clockwise
# Escape - Quit game
# P - Pause game
#
# Have fun!

# Copyright (c) 2010 "Kevin Chabowski"<kevin@kch42.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from random import choice

import sys

from src.player import Player
from src.helper import *
import src.heuristic as heuristic

# The configuration
config = {
    'cell_size': 20,
    'cols': 10,
    'rows': 20,
    'delay': 1,
    'maxfps': 30
}

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 150, 0),
    (0, 0, 255),
    (255, 120, 0),
    (255, 255, 0),
    (180, 0, 255),
    (0, 220, 220)
]

# Define the shapes of the single parts
tetris_shapes = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]


def new_board():
    board = [[0 for x in range(config['cols'])]
             for y in range(config['rows'])]
    board += [[1 for x in range(config['cols'])]]
    return board


class TetrisApp(object):
    defaultWeights = heuristic.defaultWeights

    def __init__(self, useGUI, weights=defaultWeights):
        if useGUI:
            import pygame
            pygame.init()
            pygame.key.set_repeat(250, 25)
        self.width = config['cell_size'] * config['cols']
        self.height = config['cell_size'] * config['rows']

        self.gameover = False
        self.paused = False

        self.numPieces = 0
        self.rowsCleared = 0

        self.score = 0

        self.player = Player(weights)

        if useGUI:
            import pygame
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.event.set_blocked(pygame.MOUSEMOTION)
            # We do not need
            # mouse movement
            # events, so we
            # block them.

    def new_stone_from_sequence(self, currentPieceType, nextPieceType):
        self.stone = tetris_shapes[currentPieceType]
        self.nextStone = tetris_shapes[nextPieceType]

        self.stone_x = int(config['cols'] / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0

        self.numPieces += 1

        if check_collision(self.board,
                           self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True

    def new_stone(self):
        self.stone = choice(tetris_shapes)
        self.stone_x = int(config['cols'] / 2 - len(self.stone[0]) / 2)
        self.stone_y = 0

        self.numPieces += 1

        if check_collision(self.board,
                           self.stone,
                           (self.stone_x, self.stone_y)):
            self.gameover = True

    def init_game(self):
        self.board = new_board()
        self.new_stone()

    def center_msg(self, msg):
        import pygame
        for i, line in enumerate(msg.splitlines()):
            msg_image = pygame.font.Font(
                pygame.font.get_default_font(), 12).render(
                line, False, (255, 255, 255), (0, 0, 0))

            msgim_center_x, msgim_center_y = msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2

            self.screen.blit(msg_image, (
                self.width // 2 - msgim_center_x,
                self.height // 2 - msgim_center_y + i * 22))

    def draw_matrix(self, matrix, offset):
        import pygame
        off_x, off_y = offset
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x + x) *
                            config['cell_size'],
                            (off_y + y) *
                            config['cell_size'],
                            config['cell_size'],
                            config['cell_size']), 0)

    def move(self, delta_x):
        if not self.gameover and not self.paused:
            new_x = self.stone_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > config['cols'] - len(self.stone[0]):
                new_x = config['cols'] - len(self.stone[0])
            if not check_collision(self.board,
                                   self.stone,
                                   (new_x, self.stone_y)):
                self.stone_x = new_x

    def quit(self):
        import pygame
        self.center_msg("Exiting...")
        pygame.display.update()
        sys.exit()

    def remove_row(self, board, row):
        del board[row]
        self.rowsCleared += 1
        return [[0 for i in range(config['cols'])]] + board

    def rotate_stone(self):
        if not self.gameover and not self.paused:
            new_stone = rotate_clockwise(self.stone)
            if not check_collision(self.board,
                                   new_stone,
                                   (self.stone_x, self.stone_y)):
                self.stone = new_stone

    def toggle_pause(self):
        self.paused = not self.paused

    def start_game(self):
        if self.gameover:
            self.init_game()
            self.gameover = False

    def render(self):
        import pygame
        if not self.gameover:
            self.screen.fill((0, 0, 0))

            if self.paused:
                self.center_msg("Paused")
            else:
                try:
                    self.draw_matrix(self.board, (0, 0))
                except:
                    self.gameover = True
                '''
                self.draw_matrix(self.stone,
                                     (self.stone_x,
                                   self.stone_y))
                '''
        if self.gameover:
            self.center_msg("""Game Over!
            Press space to continue""")

        pygame.display.update()

    def makeMove(self, pieceType, nextPieceType, isHillClimb=False):
        self.new_stone_from_sequence(pieceType, nextPieceType)
        self.board = self.player.play(self.board, [self.stone, self.nextStone], [pieceType, nextPieceType])

        numCleared = 0

        while True:
            for i, row in enumerate(self.board[:-1]):
                if 0 not in row:
                    self.board = self.remove_row(self.board, i)
                    numCleared += 1
                    break
            else:
                break

        self.score += pow(2,numCleared)
        if isHillClimb:
            # Check the current height of the board
            maxHeight = 0
            for h in range(config['rows']):
                if sum(self.board[h]) == 0:
                    maxHeight = config['rows'] - h
                    break
            self.score -= (maxHeight / config['rows'])
            # Make sure that score is not negative
            if self.score < 0:
                self.score = 0


    def run(self):
        import pygame
        key_actions = {
            'ESCAPE': self.quit,
            'LEFT': lambda: self.move(-1),
            'RIGHT': lambda: self.move(+1),
            'UP': self.rotate_stone,
            'p': self.toggle_pause,
            'SPACE': self.start_game
        }

        pygame.time.set_timer(pygame.USEREVENT + 1, config['delay'])
        dont_burn_my_cpu = pygame.time.Clock()
        self.board = new_board()
        self.new_stone()

        prev_count = 0

        while 1:
            self.render()

            if not self.gameover:
                # Keep track of the old stone and generate the next stone
                old_stone = self.stone
                self.new_stone()
                # Get the next move from the player
                self.board = self.player.play(self.board, [old_stone, self.stone])
                while True:
                    for i, row in enumerate(self.board[:-1]):
                        if 0 not in row:
                            self.board = self.remove_row(
                                self.board, i)
                            break
                    else:
                        break

            if (self.numPieces % 1000 == 0) and (prev_count != self.numPieces):
                prev_count = self.numPieces
                print("----- STATUS UPDATE -----")
                print("Number of pieces used: ", self.numPieces)
                print("Number of rows cleared: ", self.rowsCleared)
                print("")


            pygame.time.delay(config['delay'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print(self.board)
                    print("Number of pieces used: ", self.numPieces)
                    print("Number of rows cleared: ", self.rowsCleared)
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_"
                                             + key):
                            key_actions[key]()

            dont_burn_my_cpu.tick(config['maxfps'])

    def runSequence(self,sequence):
        import pygame
        pygame.time.set_timer(pygame.USEREVENT + 1, config['delay'])
        dont_burn_my_cpu = pygame.time.Clock()
        pieceNumber = 0

        self.board = new_board()

        while 1:
            if not self.gameover and (pieceNumber < len(sequence)-1):
                self.makeMove(sequence[pieceNumber], sequence[pieceNumber+1])
            else:
                print("Number of pieces used: ", self.numPieces)
                print("Number of rows cleared: ", self.rowsCleared)
                break

            self.render()

            pygame.time.delay(config['delay'])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Number of pieces used: ", self.numPieces)
                    print("Number of rows cleared: ", self.rowsCleared)
                    self.quit()

            dont_burn_my_cpu.tick(config['maxfps'])
            pieceNumber += 1

    def runSequenceNoGUI(self, sequence, reset=True, isHillClimb=False):
        self.board = new_board()
        for i in range(len(sequence)-1):
            pieceType = sequence[i]
            nextPiece = sequence[i+1]

            if not self.gameover:
                self.makeMove(pieceType, nextPiece, isHillClimb=isHillClimb)

        if self.gameover and reset:
            self.score = 0

        return self.score
