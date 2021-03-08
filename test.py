import board

def test_ko():

    b = board.BoardState([[board.EMPTY for i in range(4)] for j in range(4)], board.BLACK)

    b = b.place(2, 0)

    b = b.place(1, 0)

    b = b.place(3, 1)

    b = b.place(0, 1)

    b = b.place(2, 2)

    b = b.place(1, 2)

    b = b.place(1, 1)

    b = b.place(2, 1)


    # Illegal moves must return None
    assert b.place(1, 1) == None
