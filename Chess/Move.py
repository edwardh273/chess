"""
Defines the move class that is passed into the move functions of the GameState
"""
class Move:

    def __init__(self, startSq, endSq, board):  # ((startCol, startRow), (endCol, endRow), board)
        # position of mouse click is format sqSelected: (col, row)
        self.startCol = startSq[0]
        self.startRow = startSq[1]
        self.endCol = endSq[0]
        self.endRow = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        self.moveID = f"{self.startCol:01d}{self.startRow:01d}{self.endCol:01d}{self.endRow:01d}"

        self.isPawnPromotion = (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7)



    """
    Overriding the equals method. Only needed as we are using a class, would not be needed if we used strings, ints etc.
    """
    def __eq__(self, other):
        if isinstance(other, Move):  # if object other is class Move, then two moves are equivalent if their IDs are equivalent
            return self.moveID == other.moveID
        return False