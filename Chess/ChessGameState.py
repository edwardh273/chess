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

        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}

        self.whiteKingLocation = (4, 7)  # (col, row)
        self.blackKingLocation = (4, 0)  # (col, row)

        # initialise variables to store game data
        self.whiteToMove = True
        self.moveLog = []

        self.enpassantPossible = ()



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
                    self.moveFunctions[piece](r, c, moves)  # appends all moves for each pieces to list moves = []
        print([move.moveID for move in moves])
        return moves


    """
    Takes a Move as a parameter and executes it.  After making move, changes White to move parameter
    """
    def makeMove(self, move):

        self.board[move.startRow][move.startCol] = "--"
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"  # capturing the pawn
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move to undo later.

        # update the king's location
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endCol, move.endRow)
            print(self.whiteKingLocation)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endCol, move.endRow)
            print(self.blackKingLocation)


        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:  # if a pawn moves 2 squares
            self.enpassantPossible = (move.startCol, (move.startRow + move.endRow) // 2)  # enpassant possible to the square where the pawn would have moved if it had only moved 1 square.
            print("enpassant possible: " + str(self.enpassantPossible))

        self.whiteToMove = not self.whiteToMove  # swap players of the gameState


    """
    Get all pawn moves for the pawn located at row, col and add these moves to the list
    """
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn moves

            if self.board[r - 1][c] == "--":  # moving forwards
                moves.append(Move((c, r),(c, r-1), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # move 2 squares forward
                    moves.append(Move((c, r),(c, r-2), self.board))
            if c - 1 >= 0:  # capturing left (ensures not off board)
                if self.board[r - 1][c - 1][0] =='b':
                    moves.append(Move((c, r),(c-1, r-1), self.board))
                elif (c-1, r-1) == self.enpassantPossible and self.board[r][c-1][0] == 'b':
                    print(f"Adding en passant move: from ({c},{r}) to ({c-1},{r-1})")
                    moves.append(Move((c, r), (c-1, r-1), self.board, isEnpassantMove=True))
            if c + 1 <= 7:  # capturing right
                if self.board[r - 1][c + 1][0] =='b':
                    moves.append(Move((c, r),(c+1, r-1), self.board))
                elif (c+1, r-1) == self.enpassantPossible and self.board[r][c+1][0] == 'b':
                    print(f"Adding en passant move: from ({c},{r}) to ({c+1},{r-1})")
                    moves.append(Move((c, r), (c+1, r-1), self.board, isEnpassantMove=True))

        else:  # black pawn moves
            if self.board[r + 1][c] == "--":  # moving forwards
                moves.append(Move((c, r), (c, r+1), self.board))
                if r == 1 and self.board[r+2][c] == "--":  # move 2 squares forward
                    moves.append(Move((c, r), (c, r+2), self.board))
            if c - 1 >= 0:  # capturing left
                if self.board[r + 1][c - 1][0] =='w':
                    moves.append(Move((c, r),(c-1, r+1), self.board))
                elif (c-1, r+1) == self.enpassantPossible and self.board[r][c-1][0] == 'w':
                    print(f"Adding en passant move: from ({c},{r}) to ({c - 1},{r + 1})")
                    moves.append(Move((c, r), (c-1, r+1), self.board, isEnpassantMove=True))
            if c + 1 <= 7:  # capturing right
                if self.board[r + 1][c + 1][0] =='w':
                    moves.append(Move((c, r),(c+1, r+1), self.board))
                elif (c+1, r+1) == self.enpassantPossible and self.board[r][c+1][0] == 'w':
                    print(f"Adding en passant move: from ({c},{r}) to ({c+1},{r+1})")
                    moves.append(Move((c, r), (c+1, r+1), self.board, isEnpassantMove=True))

    """
        Get all Rook moves for the Rook located at row, col and add these moves to the list
    """
    def getRookMoves(self, r, c, moves):  # Rooks all move the same
        enemyColor = 'b' if self.whiteToMove == True else 'w'
        directions = ((0, -1), (0, 1), (-1, 0), (1, 0))  # left, right, up, down
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # confine the potential moves to the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # if blank, append move
                        moves.append(Move((c, r), (endCol, endRow), self.board))
                    elif endPiece[0] == enemyColor:  # hits enemy piece, append then break
                        moves.append(Move((c, r), (endCol, endRow), self.board))
                        break
                    else:  # hits own color piece
                        break
                else:  # off board
                    break

    """
    Get all Bishop moves for the Bishop located at row, col and add these moves to the list
    """
    def getBishopMoves(self, r, c, moves):
        enemyColor = 'b' if self.whiteToMove == True else 'w'
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))  # leftup, rightup, leftdown, rightdown
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # confine the potential moves to the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == '--':  # if blank, append move
                        moves.append(Move((c, r), (endCol, endRow), self.board))
                    elif endPiece[0] == enemyColor:  # hits enemy piece, append then break
                        moves.append(Move((c, r), (endCol, endRow), self.board))
                        break
                    else:  # hits own color piece
                        break
                else:  # off board
                    break

    """
    Get all Queen moves for the Queen located at row, col and add these moves to the list
    """
    def getQueenMoves(self, r, c, moves):
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)

    """
    Get all Knight moves for the Knight located at row, col and add these moves to the list
    """
    def getKnightMoves(self, r, c, moves):
        potentialMoves = ((-1, -2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2))
        allyColor = 'w' if self.whiteToMove == True else 'b'
        for m in potentialMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # confine the potential moves to the board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((c, r), (endCol, endRow), self.board))

    """
    Get all King moves for the King located at row, col and add these moves to the list
    """
    def getKingMoves(self, r, c, moves):
        potentialMoves = ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1))
        allyColor = 'w' if self.whiteToMove == True else 'b'
        for m in potentialMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # confine the potential moves to the board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((c, r), (endCol, endRow), self.board))
