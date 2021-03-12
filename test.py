import board

def test_score():
    b = board.BoardState(board.read_drawing("""
    XX..O..
    X...X.O
    .X....O."""), board.WHITE)

    # stones, territory
    assert b.score(board.BLACK) == 5 + 6
    assert b.score(board.WHITE) == 3 + 4

def test_check_move_legal():
    prev_b = board.BoardState(board.read_drawing("""
    .XO.
    XO.O
    .XO."""), board.BLACK)
    b = board.BoardState(board.read_drawing("""
    .XO.
    X.XO
    .XO."""), board.WHITE, prevBoardState=prev_b)

    # occupied
    assert not b._checkMoveLegal(1, 0)
    # empty
    assert b._checkMoveLegal(3, 0)
    # ko
    assert not b._checkMoveLegal(1, 1)
    # taken
    assert not b._checkMoveLegal(0, 0)

def test_place():
    b = board.BoardState(board.read_drawing("""
    .XO.
    XO.O
    .XO."""), board.BLACK)

    b_new = b.place(2, 1)

    assert b_new == board.BoardState(board.read_drawing("""
    .XO.
    X.XO
    .XO."""), board.WHITE, prevBoardState=b)

    assert b_new.prevBoardState == b


def test_remove_taken_pieces():
    b = board.BoardState(board.read_drawing("""
    XO.
    OXO
    .O."""), board.BLACK)

    assert b._removeTakenPieces(board.WHITE) == 0
    assert b._removeTakenPieces(board.BLACK) == 2

    assert b.board == board.read_drawing("""
    .O.
    O.O
    .O.""")

def test_suffocated():
    b = board.BoardState(board.read_drawing("""
    XO.
    OXO
    .O."""), board.BLACK)

    assert b._suffocatedLeft(board.WHITE, 1, 1)
    assert b._suffocatedRight(board.WHITE, 1, 1)
    assert b._suffocatedAbove(board.WHITE, 1, 1)
    assert b._suffocatedBelow(board.WHITE, 1, 1)
    assert b._suffocatedLeft(board.WHITE, 0, 0)
    assert b._suffocatedRight(board.WHITE, 0, 0)
    assert b._suffocatedAbove(board.WHITE, 0, 0)
    assert b._suffocatedBelow(board.WHITE, 0, 0)
    assert not b._suffocatedRight(board.BLACK, 1, 0)

def test_block_suffocated():
    b = board.BoardState(board.read_drawing("""
    .OO.
    OXXO
    XOOX"""), board.BLACK)

    # the XX in the middle of the board is suffocated
    assert b._blockSuffocated(1, 1)
    assert b._blockSuffocated(2, 1)

    # the OO in the bottom of the board is suffocated
    assert b._blockSuffocated(1, 2)
    assert b._blockSuffocated(2, 2)

    assert not b._blockSuffocated(1, 0)
    assert not b._blockSuffocated(2, 0)

def test_get_block():
    b = board.BoardState(board.read_drawing("""
    XOO
    XXO
    .O."""), board.WHITE)


    assert len(b._getBlock(0, 0)) == 3
    assert len(b._getBlock(2, 0)) == 3

    assert len(b._getBlock(1, 2)) == 1
    assert b._getBlock(2, 2) == None


def test_transpose():
    matrix = [[1, 2, 3, 4, 5], [0, 0, 0, 0, 0]]
    assert board.transpose(matrix) == [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0]]

def test_read_drawing():
    drawing = """
    XXX
    O.O
    XXO"""
    assert board.read_drawing(drawing) == [
        [board.BLACK, board.WHITE, board.BLACK],
        [board.BLACK, board.EMPTY, board.BLACK],
        [board.BLACK, board.WHITE, board.WHITE]
    ]
