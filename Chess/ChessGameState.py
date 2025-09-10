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

        # initialise variables to store game data
        self.whiteToMove = True
        self.moveLog = []


    """
    Takes a Move as a parameter and executes it.  After making move, changes White to move parameter
    """
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move to undo later.

        self.whiteToMove = not self.whiteToMove  # swap players of the gameState





