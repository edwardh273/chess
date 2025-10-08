import random
import time
from PieceScores import *

CHECKMATE = 1000
STALEMATE = 0
WhiteDepth = 4
BlackDepth = 5
nextMove = None
counter = 0

# Null-move pruning parameters
NULL_MOVE_REDUCTION = 3  # Reduce depth by this amount for null-move search
NULL_MOVE_MIN_DEPTH = 2  # Don't use null-move pruning below this depth

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
            if square != "--":
                piecePositionScore = piecePositionScores[square][row][col]
                if color == 'w':
                    score += pieceScore[piece] + piecePositionScore * .1
                elif color == 'b':
                    score -= (pieceScore[piece] + piecePositionScore * .1)
    return score


"""
The function that is called by ChessMain
"""
def findBestMove(gs, validMoves, returnQueue):
    global nextMove, counter, WhiteDepth, BlackDepth
    startTime = time.time()
    nextMove, counter = None, 0
    depth = WhiteDepth if gs.whiteToMove else BlackDepth
    validMoves.sort(reverse=True, key=lambda move: pieceCapturedFunc(move, gs))
    bestScore = findMoveNegaMaxAlphaBeta(gs, validMoves, depth, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1, True if gs.whiteToMove else False, allowNull=False)  # alpha = current max, so start lowest;  beta = current min so start highest
    endTime = time.time()
    print(f"movesSearched: {counter}     maxScore: {bestScore:.3f}     Time: {endTime - startTime:.2f}")
    returnQueue.put(nextMove)


""""
Function to sort valid moves before they are passed into alpha-beta pruning.
Likely strongest moves should be searched first for better pruning efficiency
"""
def pieceCapturedFunc(move, gameState):
    score = 0
    if move.pieceCaptured != "--":
        score += pieceScore[move.pieceCaptured[1]]
    if gameState.squareUnderAttack(move.startRow, move.startCol):
        score += pieceScore[move.pieceMoved[1]]
    return score


"""
Helper function to check if the current position is in zugzwang
(where any move weakens the position). Typically endgames with few pieces.
"""
def isZugzwangPosition(gs):
    # Simple heuristic: consider it zugzwang if there are very few pieces
    # More sophisticated detection could be added
    pieceCount = 0
    for row in gs.board:
        for square in row:
            if square != "--":
                pieceCount += 1
    return pieceCount <= 6  # Endgame threshold


"""
findNegaMaxAlphaBeta with null-move pruning.
Alpha = Best score the current player has found so far (starts at -1000)
Beta = Best score the opponent has found so far (starts at +1000)
allowNull = Whether null-move pruning is allowed in this node
"""
def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier, whiteAI, allowNull):
    global nextMove, counter, WhiteDepth, BlackDepth
    counter += 1

    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # Null-move pruning
    if (allowNull and
            depth >= NULL_MOVE_REDUCTION + 1 and  # Ensure we don't go negative
            not gs.inCheck and
            not isZugzwangPosition(gs)):

        # Make null move (switch turns without making a move)
        gs.whiteToMove = not gs.whiteToMove

        # Search with reduced depth using zero-width window
        nullScore = -findMoveNegaMaxAlphaBeta(
            gs,
            gs.getValidMoves(),  # Opponent's moves after null
            depth - NULL_MOVE_REDUCTION,
            -beta,
            -beta + 1,  # Zero-width window
            -turnMultiplier,
            whiteAI,  # Switch AI perspective
            allowNull=False  # Prevent consecutive null moves
        )

        # Undo null move
        gs.whiteToMove = not gs.whiteToMove

        # If null move causes beta cutoff, prune
        if nullScore >= beta:
            return beta

    maxScore = -CHECKMATE  # worst scenario
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier, whiteAI, allowNull=True)  # switch the alpha beta perspective.
        if score > maxScore:
            maxScore = score
            if (depth == WhiteDepth and whiteAI) or (depth == BlackDepth and not whiteAI):
                nextMove = move
                print(nextMove.moveID, f"{maxScore:.3f}")
        gs.undoMove()

        alpha = max(maxScore, alpha)  # pruning
        if alpha >= beta:  # we can stop searching here because opponent has already found a position limiting us to beta so will never let us reach this position in real play.
            break
    return maxScore


"""
Returns a random move.
"""
def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]