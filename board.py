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

def read_drawing(str):
    """
    We want to be able to take in a grid, where . represents empty,
    X represents black, and O represents white, and convert it into an array
    of BLACK, WHITE, EMPTY
    """

    grid = [[]]
    if str.startswith('\n'):
        str = str[1:]
    for letter in str:
        if letter == '\n':
            grid.append([])
        elif letter == 'X':
            grid[-1].append(BLACK)
        elif letter == 'O':
            grid[-1].append(WHITE)
        elif letter == '.':
            grid[-1].append(EMPTY)
    return transpose(grid)

def transpose(grid):
    new_grid = [[0 for i in range(len(grid))] for j in range(len(grid[0]))]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            new_grid[j][i] = grid[i][j]

    return new_grid


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

    def _getBlock(self, widthPos, heightPos):
        """ returns None if this is an empty square """

        color = self.board[widthPos][heightPos]
        if color == EMPTY:
            print("empty")
            return None

        searched = []

        # assume everything in here hasn't already been searched
        toSearch = [(widthPos, heightPos)]

        while len(toSearch) > 0:
            elem = toSearch.pop()

            neighbors = self._getNeighborsSameColor(elem[0], elem[1], exclude=searched)
            toSearch += neighbors

            searched.append(elem) # don't search this again

        return searched


    def _blockSuffocated(self, widthPos, heightPos):
        color = self.board[widthPos][heightPos]
        otherColor = not color

        if color == EMPTY:
            return None

        # First, we get the block that this piece is located in
        block = self._getBlock(widthPos, heightPos)



        # check if its suffocated, if its not we're good!

        for blockWidthPos, blockHeightPos in block:
            # If a SINGLE one of the neighbors is not suffocated in a
            # single direction, the block is not suffocated
            if not all([
                self._suffocatedLeft(otherColor, blockWidthPos, blockHeightPos),
                self._suffocatedRight(otherColor, blockWidthPos, blockHeightPos),
                self._suffocatedBelow(otherColor, blockWidthPos, blockHeightPos),
                self._suffocatedAbove(otherColor, blockWidthPos, blockHeightPos),
            ]):
                return False

        return True


    def _getNeighborsSameColor(self, widthPos, heightPos, exclude=[]):
        color = self.board[widthPos][heightPos]

        neighbors = []

        # left
        if widthPos != 0 and self.board[widthPos-1][heightPos] == color:
            neighbors.append((widthPos-1, heightPos))

        # right
        if widthPos != self.width - 1 and self.board[widthPos+1][heightPos] == color:
            neighbors.append((widthPos+1, heightPos))

        # up
        if heightPos != 0 and self.board[widthPos][heightPos-1] == color:
            neighbors.append((widthPos, heightPos-1))

        # down
        if heightPos != self.height-1 and self.board[widthPos][heightPos+1] == color:
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
