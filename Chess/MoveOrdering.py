from PieceScores import pieceScore


""""
Function to sort valid moves before they are passed into alpha-beta pruning.
Likely strongest moves should be searched first for better pruning efficiency
"""
def pieceCapturedFunc(move, gameState):
    score = 0
    if move.pieceCaptured != "--":
        score += pieceScore[move.pieceCaptured[1]]

    # if gameState is not None:
    #     if gameState.squareUnderAttack(move.start, move.startCol):
    #         score += pieceScore[move.pieceMoved[1]]

    return score