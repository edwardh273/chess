import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2
nextMove = None

"""
Returns a random move.
"""
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

"""
Finds best move based on material alone.  Written from the perspective of player = white, AI = black.
Finds the move that produces our opponent's lowest, maximum score.
Looks 2 moves ahead: the current move, and the return move.
White best score = CHECKMATE; black best score = -CHECKMATE
"""
def findBestMove(gs, validMoves):
    # from the perspective of black, worst score is CHECKMATE, best score is -CHECKMATE
    # player = white
    # AI = black

    turnMultiplier = 1 if gs.whiteToMove else -1 # default is black to move as the AI when findBestMove called => -1
    playerLowestMaxScore = CHECKMATE # start of worst case scenario for AI: a white checkmated black.
    bestMove = None

    random.shuffle(validMoves)  # to prevent rook moving side to side
    for AIMove in validMoves:
        gs.makeMove(AIMove)  # the AI makes a move
        playerMoves = gs.getValidMoves()  # for every move the AI can potentially make, make the player's move.

        # Given an AI move, find the highest scoring responding player move.
        playerMaxScore = -CHECKMATE # start of worst case scenario for player (white): black checkmated white
        for playerMove in playerMoves:
            gs.makeMove(playerMove)
            if gs.checkMate:
                score = -turnMultiplier * CHECKMATE  # now it's black to move.  Score = CHECKMATE, the best possible scenario for white.
            elif gs.staleMate:
                score = STALEMATE
            else:
                score = -turnMultiplier * scoreMaterial(gs.board) # 1 * scoreMaterial.
            if score > playerMaxScore:
                playerMaxScore = score
            gs.undoMove()

        # find lowest playerMaxScore and make the AI move that leads to the player's lowestMaxScore.
        if playerMaxScore < playerLowestMaxScore: # Anything less than +1000 (white checkmate) is better.
            playerLowestMaxScore = playerMaxScore
            bestMove = AIMove

        gs.undoMove()
    return bestMove

"""
The function that is called by ChessMain
"""
def findBestMoveMinMax(gs, validMoves):
    global nextMove
    nextMove = None
    random.shuffle(validMoves)  # to prevent rook moving side to side
    # findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    findMoveNegaMax(gs, validMoves, DEPTH, 1 if gs.whiteToMove else -1)
    return nextMove


"""
findMoveMinMax.  +ve score is good for white, -ve score is good for black.
"""
def findMoveMinMax(gs, validMoves, depth, whiteToMove: bool):
    global nextMove
    if depth == 0:
        return scoreBoard(gs)

    if whiteToMove:
        maxScore = -CHECKMATE  # worst score possible.
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth-1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


"""
findNegaMax.  Always find the maximum score for black and white.
"""
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreMaterial(gs.board)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth-1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore


"""
Score board.  +ve score is good for white, -ve score is good for black.
"""
def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif gs.staleMate:
        return STALEMATE

    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]

    return score


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
