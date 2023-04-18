import sys
import os
import random
import pygame
import time

sys.path.append(os.path.join("objects"))

from objects.GameResources import *
from utils import *
from objects import SudokuSquare
from utils import rows
pygame.init()
def Draw_Puzzle(values):
    size = 700, 700
    screen = pygame.display.set_mode(size)

    background_image = pygame.image.load("./images/sudoku-board-bare.jpg").convert()

    
    screen.blit(background_image, (0, 0))
    theSquares = []
    for y in range(9):
        for x in range(9):
            if x in (0, 1, 2):
                startX = (x * 57) + 38
            if x in (3, 4, 5):
                startX = (x * 57) + 99
            if x in (6, 7, 8):
                startX = (x * 57) + 159

            if y in (0, 1, 2):
                startY = (y * 57) + 35
            if y in (3, 4, 5):
                startY = (y * 57) + 100
            if y in (6, 7, 8):
                startY = (y * 57) + 165

            box = rows[y] + cols[x]
            string_number = values[box]
            if len(string_number) > 1 or string_number == '' or string_number == '.':
                number = None
            else:
                number = int(string_number)

            theSquares.append(SudokuSquare.SudokuSquare(number, startX, startY, "N", x, y))
        for square in theSquares:
            square.draw()
        pygame.display.update()



def play(values, result, history):
    while True:

        Draw_Puzzle(values)
        time.sleep(0.2)
        game = list(result.items())

        if len(game) == 0:
            break

        box, value = game.pop()
        values[box] = value


        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

