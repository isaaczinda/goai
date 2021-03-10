import board

def test_suffocated():
    b = board.BoardState([
        [board.BLACK, board.WHITE, board.EMPTY],
        [board.WHITE, board.BLACK, board.WHITE],
        [board.EMPTY, board.WHITE, board.EMPTY]
    ], board.BLACK)
    assert b._suffocatedLeft(board.WHITE, 1, 1)
    assert b._suffocatedRight(board.WHITE, 1, 1)
    assert b._suffocatedAbove(board.WHITE, 1, 1)
    assert b._suffocatedBelow(board.WHITE, 1, 1)
    assert b._suffocatedLeft(board.WHITE, 0, 0)
    assert b._suffocatedRight(board.WHITE, 0, 0)
    assert b._suffocatedAbove(board.WHITE, 0, 0)
    assert b._suffocatedBelow(board.WHITE, 0, 0)
    assert not b._suffocatedRight(board.BLACK, 1, 0)


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
