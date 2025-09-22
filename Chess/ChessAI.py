import random
from PieceScores import *
import time

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 2
nextMove = None
counter = 0


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
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            color = square[0]
            piece = square[1]

            if square == 'wp':
                score += pieceScore[piece] + whitePawnScore[row][col] * .1
            elif square == 'bp':
                score -= (pieceScore[piece] + blackPawnScore[row][col] * .1)

            if piece in ['B', 'N']:
                piecePositionScore = piecePositionScores[piece][row][col]
                if color == 'w':
                    score += pieceScore[piece] + piecePositionScore * .1
                elif color == 'b':
                    score -= (pieceScore[piece] + piecePositionScore * .1)

            if piece in ['Q', 'R']:
                if color == 'w':
                    score += pieceScore[piece]
                elif color == 'b':
                    score -= pieceScore[piece]

    return score


"""
The function that is called by ChessMain
"""
def findBestMove(gs, validMoves, returnQueue):
    global nextMove, counter
    startTime = time.time()
    nextMove = None
    random.shuffle(validMoves)  # to prevent rook moving side to side
    counter = 0
    bestScore = findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)  # alpha = current max, so start lowest;  beta = current min so start hightest
    endTime = time.time()
    print(f"movesSearched: {counter}     maxScore: {bestScore:.3f}     Time: {endTime - startTime:.2f}")
    returnQueue.put(nextMove)


"""
findNegaMaxAlphaBeta.  Always find the maximum score for black and white.
Alpha = Best score the current player has found so far (starts at -1000)
Beta = Best score the opponent has found so far (starts at +1000)
When beta < alpha, the maximizing player need not consider further descendants of this node, as opponent player won't let them reach it in real play.
"""
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # move ordering - implement later.  Best moves explored first are most efficient.
    maxScore = -CHECKMATE # worst scenario
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)  # switch the alpha beta perspective.
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(nextMove.moveID, f"{maxScore:.3f}")
        gs.undoMove()

        alpha = max(maxScore, alpha)  # pruning
        if beta <= alpha:  # we can stop searching here because opponent has already found a position limiting us to beta so will never let us reach this position in real play.
            break

    return maxScore


"""
Returns a random move.
"""
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]