import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0

"""
Returns a random move.
"""
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

"""
Finds best move based on material alone.  Written from the perspective of player = white, AI = black.
"""
def findBestMove(gs, validMoves):
    # white best score = CHECKMATE; black best score = -CHECKMATE
    # from the perspective of black, worst score is CHECKMATE, best score is -CHECKMATE

    # player = white
    # AI = black

    # maximising the board vs minimising the board for black vs white.
    turnMultiplier = 1 if gs.whiteToMove else -1 # default is black to move as the AI when findBestMove called => -1

    # we want to make the move that produces our opponent's lowest, maximum score.
    playerLowestMaxScore = CHECKMATE # worst case scenario for AI is a white checkmated black.
    bestMove = None

    random.shuffle(validMoves)
    for AIMove in validMoves:
        gs.makeMove(AIMove)  # the AI makes a move
        playerMoves = gs.getValidMoves()  # for every move the AI can potentially make, make the player's move.

        # Given an AI move, find the highest scoring responding player move.
        playerMaxScore = -CHECKMATE # worst case scenario for player (white) is black checkmated white
        for playerMove in playerMoves:
            gs.makeMove(playerMove)
            if gs.checkMate:
                score = -turnMultiplier * CHECKMATE
            elif gs.staleMate:
                score = STALEMATE
            score = -turnMultiplier * scoreMaterial(gs.board)
            if score > playerMaxScore:
                playerMaxScore = score
            gs.undoMove()

        if playerMaxScore < playerLowestMaxScore: # Anything less than +1000 (white checkmate) is better.
            playerLowestMaxScore = playerMaxScore
            bestMove = AIMove

        gs.undoMove()

    return bestMove


"""
Score the board based on material
"""
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -=pieceScore[square[1]]

    return score
