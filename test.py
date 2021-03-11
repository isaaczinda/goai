import board

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


    # b = b.place(2, 0)
    # print(b)
    # b = b.place(1, 0)
    # print(b)
    # b = b.place(3, 1)
    # print(b)
    # b = b.place(0, 1)
    # print(b)
    # b = b.place(2, 2)
    # print(b)
    # b = b.place(1, 2)
    # print(b)
    # b = b.place(1, 1)
    # print(b)
    # b = b.place(2, 1)
    # print(b)

    # # Illegal moves must return None
    # assert b.place(1, 1) == None

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
