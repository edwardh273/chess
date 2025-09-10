"""
This is the main driver file.  It will be responsible for handling user input and displaying the current GameState object.
"""
import pygame as p
import os
from ChessGameState import GameState
from Move import Move

WIDTH = HEIGHT = 512
DIMENSION = 8  # dimensions of chess board = 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animation later on
IMAGES = {}
CHESS_DIR = os.path.dirname(__file__)

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

    # setup variables
    moveMade = False
    gs = GameState()  # initialize the GameState, whiteToMove = True
    print()
    print("white to move: " + str(gs.whiteToMove))
    sqSelected = ()  # no square is selected initially.  Keeps track of last click of user (tuple: (col, row))
    playerClicks = []  # keep track of player clicks (two tuples: [(4, 7), (4, 5)])


    allMoves = gs.getValidMoves()

    while running:
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                # pygame .get_pos is opposite to how you slice the array of the gs.board
                location = p.mouse.get_pos()  # (col, row): (0,0)==top left;   (col=0, row=7)==bottom left;     (7, 7)==bottom right
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if sqSelected == (col, row):  # the user clicked  the same square twice
                    sqSelected = ()  # deselect
                    playerClicks = []  # reset
                    print("user clicked same square twice, reset playerClicks")

                else:
                    sqSelected = (col, row)
                    playerClicks.append(sqSelected)
                    print("player clicked square {}".format(sqSelected))

                if len(playerClicks) == 2:  # if a user has made their second click, update the board and clear playerClicks
                    print("2 clicks: attempt move:")
                    print(playerClicks)
                    moveAttempt = Move(playerClicks[0], playerClicks[1], gs.board)  # creates object of class Move(startSq, endSq, board)
                    for i in range(len(allMoves)):
                        if moveAttempt == allMoves[i]:  # if move is in all moves, make move, change moveMade variable, clear playerClicks.
                            gs.makeMove(allMoves[i])
                            print([move.moveID for move in gs.moveLog])
                            moveMade = True
                            print()
                            print("white to move: " + str(gs.whiteToMove))
                            sqSelected = ()
                            playerClicks = []
                    if not moveMade:  # if len(playerClicks == 2) but move not a valid move, clear playerClicks
                        sqSelected = ()
                        playerClicks = []
                        print(playerClicks)

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed.
                    gs.undoMove()
                    print('Undone move')
                    print([move.moveID for move in gs.moveLog])
                    moveMade = True


        if moveMade:  # only calculate new moves after each turn, not each frame.
            allMoves = gs.getValidMoves()
            moveMade = False  # set back to False

        drawGameState(screen, gs)  # can I delay this to once every move made?
        clock.tick(MAX_FPS)  # sets frame rate of game, is called once per frame.
        p.display.flip()  # updates the full display Surface to the screen.













"""
Initialize a global dictionary of images. This will be called exactly once in the main
"""
def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bp", "wp", "wR", "wN", "wB", "wQ", "wK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(CHESS_DIR + '/images/' + piece + '.png'),
                                          (SQ_SIZE, SQ_SIZE))  # Note: we can access an image by saying "IMAGES['wp']"


"""
Responsible for all the graphics within a current gamestate.
"""
def drawGameState(screen, gs):
    drawBoard(screen)  # draw squares on the board
    drawPieces(screen, gs.board)  # draw pieces on top of those squares

"""
Draws the squares on the board.  The top left square is always light.
"""
def drawBoard(screen):
    colors = [p.Color('whitesmoke'), p.Color('gray50')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Draw the pieces on the board using the current GameState.board
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], (c*SQ_SIZE,r*SQ_SIZE))


# run main
main()