# make object that represents board state **
#  - place() --> board state
# SERIALIZABLE


# hard parts:
#  - list of places you can't go
#  - whether the game is over


# def StartOfGameBoard()
#     [[EMPTY for w in range(width)] for h in range(height)]

import copy

# values for empty, black, white
BLACK = 0
WHITE = 1
EMPTY = 2


class BoardState:
    def __init__(self, board, turn, prevBoardState=None):

        # board[width][height]
        self.board = board

        self.height = len(board[0])
        self.width = len(board)

        # turn = 1 if it's black turn, 2 if it's white's turn
        self.turn = turn

        self.prevBoardState = prevBoardState

    def __repr__(self):
        str = ""
        for h in range(self.height):
            for w in range(self.width):
                if self.board[w][h] == EMPTY:
                    str += "."
                elif self.board[w][h] == BLACK:
                    str += "X"
                elif self.board[w][h] == WHITE:
                    str += "O"
            str += "\n"
        if self.turn == BLACK:
            str += "Black's turn\n\n"
        else:
            str += "White's turn\n\n"
        return str

    def __eq__(self, other):
        if not isinstance(other, BoardState):
            return False

        return self.turn == other.turn and self.board == other.board

    def __leftOccupied(self, color, widthPos, heightPos):
        if widthPos == 0:
            return True

        return self.board[widthPos][heightPos] == color


    def __rightOccupied(self, color, widthPos, heightPos):
        if widthPos == self.width-1:
            return True

        return self.board[widthPos][heightPos] == color

    def __aboveOccupied(self, color, widthPos, heightPos):
        if heightPos == 0:
            return True

        return self.board[widthPos][heightPos] == color

    def __belowOccupied(self, color, widthPos, heightPos):
        if heightPos == self.height-1:
            return True

        return self.board[widthPos][heightPos] == color


    def legalMoves(self):
        """ Returns positions on the board which are empty and
        aren't surrounded. """

        areEmpty = [[item == EMPTY for item in row] for row in self.board]


        # check if the spot is surrounded by the color that is not
        # about to place

        otherColor = not self.turn

        for w in range(self.width):
            for h in range(self.height):
                if self.__leftOccupied(otherColor, w, h) and self.__rightOccupied(otherColor, w, h) and self.__aboveOccupied(otherColor, w, h) and self.__belowOccupied(otherColor, w, h):
                    areEmpty[w][h] = False

        return areEmpty


    def place(self, widthPos, heightPos):
        """ Returns new board state. If move was not legal,
        returns None. """

        if not self.legalMoves()[widthPos][heightPos]:
            return None

        newBoard = copy.deepcopy(self.board)
        newBoard[widthPos][heightPos] = self.turn

        newState = BoardState(newBoard, not self.turn, prevBoardState=self)

        # now check to make sure this move doesn't repeat what the board
        # state was 2 turns ago. Since self is ~now~ 1 board state ago, we
        # just have to check self.prevBoardState.

        if self.prevBoardState != None and self.prevBoardState == newState:
            return None

        return newState


if __name__ == '__main__':
    test()
