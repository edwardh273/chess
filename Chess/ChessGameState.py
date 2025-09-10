from Move import Move

"""
This class is responsible for storing all the information about the current
state of a chess game.  It will also be responsible for determining the valid
moves at the current state.  It will also keep a move log.
"""
class GameState:
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.moveFunctions ={'p': self.getPawnMoves}

        # initialise variables to store game data
        self.whiteToMove = True
        self.moveLog = []



    """
    Iterates through all pieces of the board, calculating possible moves for every piece of the color of whose turn it is.
    """
    def getAllPossibleMoves(self):
        print("getting all possible moves")
        moves = []  # ((startCol, startRow), (endCol, endRow), board)
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of cols in given row
                color, piece = self.board[r][c][0], self.board[r][c][1]
                if (color =='b' and self.whiteToMove == False) or (color =='w' and self.whiteToMove== True):  # if the piece is black, and it's black's turn, or if piece is white, and it's white's turn:
                    if piece == 'p':
                        self.moveFunctions[piece](r, c, moves)  # appends all moves for each pieces to list moves = []
        print([move.moveID for move in moves])
        return moves


    """
    Takes a Move as a parameter and executes it.  After making move, changes White to move parameter
    """
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move to undo later.

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        self.whiteToMove = not self.whiteToMove  # swap players of the gameState



    """
    Get all pawn moves for the pawn located at row, col and add these moves to the list
    """
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves
            if self.board[r - 1][c] == "--":  # moving forwards
                moves.append(Move((c, r),(c, r-1), self.board))
                if r == 6 and self.board[r-2][c] == "--":  # move 2 squares forward
                    moves.append(Move((c, r),(c, r-2), self.board))
            if c - 1 >= 0:  # capturing left (ensures not off board)
                if self.board[r - 1][c - 1][0] =='b':
                    moves.append(Move((c, r),(c-1, r-1), self.board))
            if c + 1 <= 7:  # capturing right
                if self.board[r - 1][c + 1][0] =='b':
                    moves.append(Move((c, r),(c+1, r-1), self.board))

        else:  # black pawn moves
            if self.board[r + 1][c] == "--":  # moving forwards
                moves.append(Move((c, r), (c, r+1), self.board))
                if r == 1 and self.board[r+2][c] == "--":  # move 2 squares forward
                    moves.append(Move((c, r), (c, r+2), self.board))
            if c - 1 >= 0:  # capturing left
                if self.board[r + 1][c - 1][0] =='w':
                    moves.append(Move((c, r),(c-1, r+1), self.board))
            if c + 1 <= 7:  # capturing right
                if self.board[r + 1][c + 1][0] =='w':
                    moves.append(Move((c, r),(c+1, r+1), self.board))


