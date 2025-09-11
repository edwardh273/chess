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

    # setup variables
    running = True
    moveMade = False
    gameOver = False
    gs = GameState()  # initialize the GameState, whiteToMove = True
    print()
    print("white to move: " + str(gs.whiteToMove))
    sqSelected = ()  # no square is selected initially.  Keeps track of last click of user (tuple: (col, row))
    playerClicks = []  # keep track of player clicks (two tuples: [(4, 7), (4, 5)])

    validMoves = gs.getValidMoves()

    while running:
        for e in p.event.get():

            if e.type == p.QUIT:
                running = False

            elif e.type == p.MOUSEBUTTONDOWN:
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
                        print("player clicked square {}".format(sqSelected))

                    if len(playerClicks) == 2:  # if a user has made their second click, update the board and clear playerClicks
                        print("2 clicks: attempt move:")
                        print(playerClicks)
                        moveAttempt = Move(playerClicks[0], playerClicks[1], gs.board)  # creates object of class Move(startSq, endSq, board)
                        for i in range(len(validMoves)):
                            if moveAttempt == validMoves[i]:  # if move is in all moves, make move, change moveMade variable, clear playerClicks.
                                gs.makeMove(validMoves[i])
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
            animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False  # set back to False

        drawGameState(screen, gs, validMoves, sqSelected)  # can I delay this to once every move made?

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins by checkmate")
            else:
                drawText(screen, "White wins by checkmate")
        elif gs.staleMate:
            gameOver = True
            drawText(screen, "Stalemate")



        clock.tick(MAX_FPS)  # sets frame rate of game, is called once per frame.
        p.display.flip()  # updates the full display Surface to the screen.


"""
Highlight sq selected and available moves.
"""
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        c, r = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):  # square selected is a piece of the person which turn it is
            surface = p.Surface((SQ_SIZE, SQ_SIZE))
            surface.set_alpha(100)  # transparency value
            surface.fill(p.Color("blue"))
            screen.blit(surface, (c*SQ_SIZE, r*SQ_SIZE))
            # highlight valid moves from that square
            surface.fill(p.Color("yellow"))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(surface, (SQ_SIZE * move.endCol, SQ_SIZE * move.endRow))


"""
Animating a move
"""
def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10  # frame to move 1 sq
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        c, r = (move.startCol + dC*frame/frameCount, move.startRow + dR*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        color = colors[(move.endCol + move.endRow) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)


"""
Finish text
"""
def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)


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
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)  # draw pieces on top of those squares

"""
Draws the squares on the board.  The top left square is always light.
"""
def drawBoard(screen):
    global colors
    colors = [p.Color('whitesmoke'), p.Color('gray50')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


"""
Draw the pieces on the board using the current GameState.board
"""
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], (c*SQ_SIZE,r*SQ_SIZE))


if __name__ == "__main__":
    main()