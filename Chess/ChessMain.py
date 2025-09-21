"""
This is the main driver file.  It will be responsible for handling user input and displaying the current GameState object.
"""
import multiprocessing as mp
from ChessGameState import GameState
from ChessAI import findBestMove
from Move import Move
from DisplayFuncs import *

WIDTH = HEIGHT = 768
DIMENSION = 8  # dimensions of chess board = 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 30  # for animation later on
IMAGES = {}
CHESS_DIR = os.path.dirname(__file__)
colors = []

"""
The main driver for our code.  This will handle user input and updating the graphics.
"""
def main():
    # set up the game
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    loadImages()  # only do this once before the while loop

    # setup variables
    running = True
    moveMade = False
    gameOver = False
    gs = GameState()  # initialize the GameState, whiteToMove = True
    sqSelected = ()  # no square is selected initially.  Keeps track of last click of user (tuple: (col, row))
    playerClicks = []  # keep track of player clicks (two tuples: [(4, 7), (4, 5)])

    playerOne = True  # if a human is playing white, then True.  If AI is playing, then false
    playerTwo = False  # same as above, but for black.

    validMoves = gs.getValidMoves()
    print()
    print("white to move: " + str(gs.whiteToMove))

    while running:

        isHumanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)

        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
                if isHumanTurn:
                    if not gameOver:
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

                        if len(playerClicks) == 2:  # if a user has made their second click, update the board and clear playerClicks
                            print("2 clicks: attempt move:")
                            print(playerClicks)
                            moveAttempt = Move(playerClicks[0], playerClicks[1], gs.board)  # creates object of class Move(startSq, endSq, board)
                            for i in range(len(validMoves)):
                                if moveAttempt == validMoves[i]:  # if move is in all moves, make move, change moveMade variable, clear playerClicks.
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    sqSelected = ()
                                    playerClicks = []
                            if not moveMade:  # if len(playerClicks == 2) but move not a valid move, clear playerClicks
                                sqSelected = ()
                                playerClicks = []
                                print(playerClicks)

            elif e.type == p.KEYDOWN:
                if e.key == p.K_z and len(gs.moveLog) > 0:  # undo when 'z' is pressed.
                    if playerOne and playerTwo:  # if both human players, undo the last human move
                        gs.undoMove()
                        validMoves = gs.getValidMoves()
                        gameOver = False
                    if playerOne and not playerTwo:  # if only white human player
                        gs.undoMove()
                        gs.undoMove()
                        validMoves = gs.getValidMoves()
                        gameOver = False

        if gameOver:  # end of game logic
            if gs.inCheck():
                if gs.whiteToMove:
                    drawText(screen, "Black wins by checkmate")
                else:
                    drawText(screen, "White wins by checkmate")
            else:
                drawText(screen, "Stalemate")


        # ChessAI logic
        if not isHumanTurn and not gameOver:
            AIMove = findBestMove(gs, validMoves)
            if AIMove is not None:
                gs.makeMove(AIMove)
                moveMade = True
            else:
                gameOver = True

        if moveMade:  # only calculate new moves after each turn, not each frame.
            animateMove(gs.moveLog[-1], screen, gs.board, clock)
            print([move.moveID for move in gs.moveLog])
            print()
            print("white to move: " + str(gs.whiteToMove))
            validMoves = gs.getValidMoves()
            moveMade = False  # set back to False



        clock.tick(MAX_FPS)  # sets frame rate of game, is called once per frame.
        p.display.flip()  # updates the full display Surface to the screen.
        drawGameState(screen, gs, validMoves, sqSelected)


if __name__ == "__main__":
    main()