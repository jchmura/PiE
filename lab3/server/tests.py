import unittest

from server.game.tic_tac_toe import Board, Sign


class TestTicTacToeBoard(unittest.TestCase):
    def test_initial_board(self):
        board = Board()
        b = board.board

        self.assertEqual(3, len(b))
        for row in b:
            self.assertEqual(3, len(row))
            for item in row:
                self.assertEqual(Sign.empty, item)

    def test_not_finished(self):
        board = Board()
        self.assertFalse(board.finished)

        b = board.board
        b[0][1] = Sign.x
        b[1][1] = Sign.o
        b[2][0] = Sign.o
        board.board = b
        self.assertFalse(board.finished)

    def test_finished(self):
        board = Board()
        b = board.board
        b[0][1] = Sign.x
        b[1][1] = Sign.x
        b[2][1] = Sign.x
        board.board = b
        self.assertTrue(board.finished)

    def test_won_x(self):
        board = Board()
        b = board.board
        b[0][1] = Sign.x
        b[1][1] = Sign.x
        b[2][1] = Sign.x
        board.board = b
        self.assertTrue(board.won(Sign.x))

    def test_won_o(self):
        board = Board()
        b = board.board
        b[0][0] = Sign.o
        b[1][1] = Sign.o
        b[2][2] = Sign.o
        board.board = b
        self.assertTrue(board.won(Sign.o))

    def test_won_column(self):
        board = Board()
        b = board.board
        b[0][0] = Sign.o
        b[0][1] = Sign.o
        b[0][2] = Sign.o
        board.board = b
        self.assertTrue(board.won(Sign.o))

    def test_tie(self):
        board = Board()
        x, o = Sign.x, Sign.o
        board.board = [[x, x, o], [o, o, x], [x, o, o]]
        self.assertTrue(board.tie())

    def test_put(self):
        board = Board()
        x, y = 2, 1
        board.put(x, y, Sign.x)
        self.assertEqual(Sign.x, board.board[x][y])

    def test_put_not_sign(self):
        board = Board()
        self.assertRaises(ValueError, board.put, 1, 1, 'x')

    def test_put_outside(self):
        board = Board()
        self.assertRaises(IndexError, board.put, 3, 1, Sign.x)

    def test_put_already_filled(self):
        board = Board()
        x, y = 1, 1
        board.put(x, y, Sign.x)
        self.assertRaises(IndexError, board.put, x, y, Sign.x)

    def test_assign_wrong_column_length(self):
        board = Board()
        x, o = Sign.x, Sign.o
        self.assertRaises(ValueError, setattr, board, "board", [[x, o]])

    def test_assign_wrong_row_length(self):
        board = Board()
        x, o = Sign.x, Sign.o
        self.assertRaises(ValueError, setattr, board, "board", [[x, o, o], [x, o], [x, x, o, x]])

    def test_assign_wrong_sign(self):
        board = Board()
        x, o = Sign.x, Sign.o
        self.assertRaises(ValueError, setattr, board, "board", [[x, x, o], [x, o, o], [o, o, 3]])