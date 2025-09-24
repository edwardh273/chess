import random
from PieceScores import *
import time

CHECKMATE = 1000
STALEMATE = 0
WhiteDepth = 3
BlackDepth = 3
nextMove = None
counter = 0
counterBreak = 0


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

            if square in ['wp', 'bp', 'wB', 'bB', 'wN', 'bN', 'wK', 'bK']:
                piecePositionScore = piecePositionScores[square][row][col]
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
def findBestMove(gs, validMoves, returnQueue, whiteMoveList, blackMoveList):
    global nextMove, counter, counterBreak
    startTime = time.time()
    nextMove = None
    random.shuffle(validMoves)  # to prevent rook moving side to side
    counter = 0
    counterBreak = 0
    depth = WhiteDepth if gs.whiteToMove else BlackDepth

    if gs.whiteToMove:
        if len(whiteMoveList) > 1 and whiteMoveList[-2] in validMoves:
            print("---------changing move order for white---------")
            tmpMove0 = validMoves[0]
            validMoves[validMoves.index(whiteMoveList[-2])] = tmpMove0
            validMoves[0] = whiteMoveList[-2]
    else:
        if len(blackMoveList) > 1 and blackMoveList[-2] in validMoves:
            print("---------changing move order for black---------")
            tmpMove0 = validMoves[0]
            validMoves[validMoves.index(blackMoveList[-2])] = tmpMove0
            validMoves[0] = blackMoveList[-2]

    bestScore = findMoveNegaMaxAlphaBeta(gs, validMoves, depth, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1, True if gs.whiteToMove else False, whiteMoveList, blackMoveList)  # alpha = current max, so start lowest;  beta = current min so start hightest
    endTime = time.time()
    print(f"movesSearched: {counter}     maxScore: {bestScore:.3f}     Time: {endTime - startTime:.2f}     branchesBrokenOutOf: {counterBreak}")
    returnQueue.put((nextMove, whiteMoveList, blackMoveList))


"""
findNegaMaxAlphaBeta.  Always find the maximum score for black and white.
Alpha = Best score the current player has found so far (starts at -1000)
Beta = Best score the opponent has found so far (starts at +1000)
When beta < alpha, the maximizing player need not consider further descendants of this node, as opponent player won't let them reach it in real play.
"""
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier, whiteAI, whiteMoveList, blackMoveList):
    global nextMove, counter, WhiteDepth, BlackDepth, counterBreak
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE # worst scenario
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier, whiteAI, whiteMoveList, blackMoveList)  # switch the alpha beta perspective.
        if score > maxScore:
            maxScore = score
            if (depth == WhiteDepth and whiteAI) or (depth == BlackDepth and not whiteAI):
                nextMove = move
                print(nextMove.moveID, f"{maxScore:.3f}")
                whiteMoveList.append(nextMove) if whiteAI else blackMoveList.append(nextMove)
        gs.undoMove()

        alpha = max(maxScore, alpha)  # pruning
        if beta <= alpha:  # we can stop searching here because opponent has already found a position limiting us to beta so will never let us reach this position in real play.
            counterBreak += 1
            break

    return maxScore


"""
Returns a random move.
"""
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]