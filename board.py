# TODO:
# - whether the game is over
# - when does AI pass (no more legal moves)

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

    # # def __removeTakenPieces(self):
    #     ''' returns (new cleaned up board state, number pieces removed) '''

    def _blockSuffocated(self, otherColor, widthPos, heightPos):
        checked = []

        toCheck = []

        # enqueue 1

        # check if its suffocated, if its not we're good!
        if not all([
            self._suffocatedLeft(otherColor, widthPos, heightPos),
            self._suffocatedRight(otherColor, widthPos, heightPos),
            self._suffocatedBelow(otherColor, widthPos, heightPos),
            self._suffocatedAbove(otherColor, widthPos, heightPos),
        ]):
            return False

        # If it is suffocated, check its neighbors
        neighbors = self._getNeighbors(widthPos, heightPos, checked)



        # If there aren't neighbors, its a singleton OR they've all been
        # checked
        if len(neighbors) == 0:
            return True

        for neighbor in neighbors:
            # If
            if not self._blockSuffocated(otherColor, neighbor[0], neighbor[1]):
                return False



        [ for neighbor in neighbors]


    def _getNeighbors(self, widthPos, heightPos, exclude=[]):
        color = self.board[widthPos][heightPos]

        neighbors = []

        # left
        if widthPos != 0:
            neighbors.append((widthPos-1, heightPos))

        # right
        if widthPos != self.width - 1:
            neighbors.append((widthPos+1, heightPos))

        # up
        if heightPos != 0:
            neighbors.append((widthPos, heightPos-1))

        # down
        if heightPos != self.height-1:
            neighbors.append((widthPos, heightPos+1))

        # remove excluded ones
        return [t for t in neighbors if t not in exclude]


    def _suffocatedLeft(self, otherColor, widthPos, heightPos):
        # Returns True if we hit the left wall of the board
        if widthPos == -1:
            return True

        # If we hit our own color, keep going
        if self.board[widthPos][heightPos] == (not otherColor):
            return self._suffocatedLeft(otherColor, widthPos-1, heightPos)

        # If we hit the other color, it is suffocated
        if self.board[widthPos][heightPos] == otherColor:
            return True

        # Otherwise it's empty so we return False
        return False


    def _suffocatedRight(self, otherColor, widthPos, heightPos):
        # Returns True if we hit the left wall of the board
        if widthPos == self.width:
            return True

        # If we hit our own color, keep going
        if self.board[widthPos][heightPos] == (not otherColor):
            return self._suffocatedRight(otherColor, widthPos+1, heightPos)

        # If we hit the other color, it is suffocated
        if self.board[widthPos][heightPos] == otherColor:
            return True

        # Otherwise it's empty so we return False
        return False

    def _suffocatedAbove(self, otherColor, widthPos, heightPos):
        # Returns True if we hit the left wall of the board
        if heightPos == -1:
            return True

        # If we hit our own color, keep going
        if self.board[widthPos][heightPos] == (not otherColor):
            return self._suffocatedAbove(otherColor, widthPos, heightPos-1)

        # If we hit the other color, it is suffocated
        if self.board[widthPos][heightPos] == otherColor:
            return True

        # Otherwise it's empty so we return False
        return False

    def _suffocatedBelow(self, otherColor, widthPos, heightPos):
        # Returns True if we hit the left wall of the board
        if heightPos == self.height:
            return True

        # If we hit our own color, keep going
        if self.board[widthPos][heightPos] == (not otherColor):
            return self._suffocatedBelow(otherColor, widthPos, heightPos+1)

        # If we hit the other color, it is suffocated
        if self.board[widthPos][heightPos] == otherColor:
            return True

        # Otherwise it's empty so we return False
        return False

    def legalMoves(self):
        """ Returns positions on the board which are empty and
        aren't surrounded. """

        areEmpty = [[item == EMPTY for item in row] for row in self.board]


        # check if the spot is surrounded by the color that is not
        # about to place

        otherColor = not self.turn

        for w in range(self.width):
            for h in range(self.height):
                # Checks if this shit's surrounded, its not a legal move if
                # surrounded. HOWEVER, it IS legal to play in a surrounded
                # area if you take an opponent's piece.
                if all([
                    self.__stoneToLeft(otherColor, w, h),
                    self.__stoneToRight(otherColor, w, h),
                    self.__stoneAbove(otherColor, w, h),
                    self.__stoneBelow(otherColor, w, h),
                    self.__removeTakenPieces()[1] == 0
                ]):
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

        # Now "take" the pieces
        newState, _ = newState.__removeTakenPieces()

        # now check to make sure this move doesn't repeat what the board
        # state was 2 turns ago. Since self is ~now~ 1 board state ago, we
        # just have to check self.prevBoardState.

        if self.prevBoardState != None and self.prevBoardState == newState:
            return None

        return newState

    def score(self, color):
        # count up my own stones
        numStones = sum([sum([elem == color for elem in row]) for row in self.board])

        # count empty terratory that we occupy




if __name__ == '__main__':
    test()
