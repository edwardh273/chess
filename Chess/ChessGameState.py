from Move import Move, CastleRights

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
        self.checkMate = False
        self.staleMate = False

        self.enpassantPossible = ()
        self.enpassantPossibleLog = [self.enpassantPossible]

        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]  # initial log is [(T, T, T, T)]


    """
    Iterates through all pieces of the board, calculating possible moves for every piece of the color of whose turn it is.
    """
    def getAllPossibleMoves(self):
        moves = []  # ((startCol, startRow), (endCol, endRow), board)
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of cols in given row
                color, piece = self.board[r][c][0], self.board[r][c][1]
                if (color =='b' and self.whiteToMove == False) or (color =='w' and self.whiteToMove== True):  # if the piece is black, and it's black's turn, or if piece is white, and it's white's turn:
                    self.moveFunctions[piece](r, c, moves)  # appends all moves for each pieces to list moves = []
        return moves


    """
    All moves considering check
    """
    def getValidMoves(self):
        tempCastleRights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)  # since some generated moves will move the Kind/Rooks
        tmpEnpassantPossible = self.enpassantPossible # tuples are immutable so we are grabbing the value of it, not a reference to that object.

        moves = self.getAllPossibleMoves()

        # to generate castle moves
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[1], self.whiteKingLocation[0], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[1], self.blackKingLocation[0], moves)

        # remove moves that leave you in check
        for i in range(len(moves) -1, -1, -1):  # When removing from a list, go backwards through that list, up to (not including) -1.
            self.makeMove(moves[i])  # make move, switch to black's perspective.
            self.whiteToMove = not self.whiteToMove  # flip back to white's perspective for inCheck function
            if self.inCheck():
                moves.remove(moves[i])  # if in check, remove that move from all possible moves
            self.whiteToMove = not self.whiteToMove  # back to black's perspective
            self.undoMove()  # back to white's perspective

        if len(moves) == 0:  # either checkmate or stalemate
            if self.inCheck():
                self.checkMate = True
                print("--------------checkmate discovered----------------")
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False

        self.enpassantPossible = tmpEnpassantPossible
        self.currentCastlingRights = tempCastleRights

        return moves


    """
    Undo the last move made
    """
    def undoMove(self):
        if len(self.moveLog) != 0:  # make sure that there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            #update king's location
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startCol, move.startRow)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startCol, move.startRow)

            self.whiteToMove = not self.whiteToMove #swap players back

            # undo enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--' # leave landing sq blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endCol, move.endRow)
            # undo a 2 sq pawn advance
            if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
                self.enpassantPossible = ()

            # move rook back if a castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:  # kingside
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = "--"  # remove the old rook

                elif move.endCol - move.startCol == - 2:  # queenside
                    self.board[move.endRow][move.endCol -2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"

            # undo castling rights
            self.castleRightsLog.pop() # get rid of castle rights from move we are undoing.
            lastCastleRights = self.castleRightsLog[-1]
            self.currentCastlingRights = CastleRights(lastCastleRights.wks, lastCastleRights.bks, lastCastleRights.wqs, lastCastleRights.bqs)  # reinitialize castle rights to not make a copy

            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]


            self.checkMate = False
            self.staleMate = False


    """
    Takes a Move as a parameter and executes it.  After making move, changes White to move parameter
    """
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move to undo later.

        # update the king's location
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endCol, move.endRow)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endCol, move.endRow)

        # pawn promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # enpassant
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:  # if a pawn moves 2 squares
            self.enpassantPossible = (move.startCol, (move.startRow + move.endRow) // 2)  # enpassant possible to the square where the pawn would have moved if it had only moved 1 square.
        else:
            self.enpassantPossible = ()
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"  # capturing the pawn

        # castling
        if move.isCastleMove:
            if move.endCol - move.startCol == 2:  # to the right: king side castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]  # copy the rook to the new square
                self.board[move.endRow][move.endCol + 1] = "--"  # remove the old rook

            elif move.endCol - move.startCol == -2:  # to the left: queen side castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = "--"

        self.updateCastleRights(move)  # update the castling rights whenever it's a rook or a king move
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))

        self.enpassantPossibleLog.append(self.enpassantPossible)

        self.whiteToMove = not self.whiteToMove  # swap players of the gameState

    """
    Update the castle rights given a move
    """
    def updateCastleRights(self, move):
        # check if the king moved or the rock moved
        if move.pieceMoved == "wK":
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == "bK":
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:  # whites left rock
                    self.currentCastlingRights.wqs = False
                if move.startCol == 7:  # whites right rock
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:  # black left rock
                    self.currentCastlingRights.bqs = False
                if move.startCol == 7:  # black right rock
                    self.currentCastlingRights.bks = False
        # check if the rock is captured
        if move.pieceCaptured == "wR":
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceCaptured == "bR":
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.bks = False


    """
    Determines whether the CURRENT player is in check.  Returns True, False
    """
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[1], self.whiteKingLocation[0])  # (col, row) -> r, c
        else:
            return self.squareUnderAttack(self.blackKingLocation[1], self.blackKingLocation[0])


    """
    Get all castle moves
    """
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c): return  # check if the king is inCheck as the king can't escape the check by castling
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):  # kingside
            self.getKingSideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):  # queenside
            self.getQueenSideCastleMoves(r, c, moves)

    def getKingSideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == "--" and self.board[r][c + 2] == "--":
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((c, r), (c+2, r), self.board, isCastleMove=True))

    def getQueenSideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == "--" and self.board[r][c - 2] == "--" and self.board[r][c - 3] == "--":
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):  # only squares king moves through need to not be under attack.
                moves.append(Move((c, r), (c-2, r), self.board, isCastleMove=True))


    """
    Determine if the enemy can attack the square r, c.  Returns True, False
    """
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # switch to black's perspective
        oppMoves = self.getAllPossibleMoves()  # stores all possible opponents moves
        self.whiteToMove = not self.whiteToMove  # switch turns back to white
        for oppMove in oppMoves:
            if oppMove.endRow == r and oppMove.endCol == c:
                return True
        return False


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
                    moves.append(Move((c, r), (c-1, r-1), self.board, isEnpassantMove=True))
            if c + 1 <= 7:  # capturing right
                if self.board[r - 1][c + 1][0] =='b':
                    moves.append(Move((c, r),(c+1, r-1), self.board))
                elif (c+1, r-1) == self.enpassantPossible and self.board[r][c+1][0] == 'b':
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
                    moves.append(Move((c, r), (c-1, r+1), self.board, isEnpassantMove=True))
            if c + 1 <= 7:  # capturing right
                if self.board[r + 1][c + 1][0] =='w':
                    moves.append(Move((c, r),(c+1, r+1), self.board))
                elif (c+1, r+1) == self.enpassantPossible and self.board[r][c+1][0] == 'w':
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
