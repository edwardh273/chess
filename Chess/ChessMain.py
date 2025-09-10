"""
This is the main driver file.  It will be responsible for handling user input and displaying the current GameState object.
"""
import pygame as p
import os

WIDTH = HEIGHT = 512
DIMENSION = 8  # dimensions of chess board = 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animation later on
IMAGES = {}

CHESS_DIR = os.path.dirname(__file__)

"""
Initialize a global dictionary of images. This will be called exactly once in the main
"""


def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wp", "wR", "wN", "wB", "wQ", "wK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(CHESS_DIR + '/images/' + piece + '.png'),
                                          (SQ_SIZE, SQ_SIZE))  # Note: we can access an image by saying "IMAGES['wp']"


"""
The main driver for our code.  This will handle user input and updating the graphics.
"""


def main():
    # set up the game
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    loadImages()  # only do this once before the while loop
    running = True

    while running:

        for e in p.event.get():
            if e.type == p.QUIT:
                running = False


        drawGameState(screen)  # can I delay this to once every move made?
        clock.tick(MAX_FPS)  # sets frame rate of game, is called once per frame.
        p.display.flip()  # updates the full display Surface to the screen.


"""
Responsible for all the graphics within a current gamestate.
"""


def drawGameState(screen):
    drawBoard(screen)  # draw squares on the board


"""
Draws the squares on the board.  The top left square is always light.
"""


def drawBoard(screen):
    colors = [p.Color('whitesmoke'), p.Color('gray50')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))



main()