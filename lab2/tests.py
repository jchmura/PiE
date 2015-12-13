import logging
import unittest
from unittest.mock import patch, Mock

from common.configuration import Configuration
from common.game import Board, Sign
from common.message import Message

from common.socket_wrapper import SocketWrapper, MSG_SIZE


class TestSocketWrapper(unittest.TestCase):
    class SocketMock:
        def __init__(self):
            self.payload = None

        def send(self, data):
            self.payload = data
            return len(data)

        def recv(self, size):
            return self.payload

    def test_pass_through(self):
        sock = TestSocketWrapper.SocketMock()
        wrapper = SocketWrapper(sock)
        data = 'some data'
        wrapper.send(data)
        received = wrapper.receive()
        self.assertEqual(data, received)

    def test_message_size(self):
        sock = TestSocketWrapper.SocketMock()
        wrapper = SocketWrapper(sock)
        data = 'some data'
        wrapper.send(data)

        self.assertEqual(MSG_SIZE, len(sock.payload))

    def test_not_sent_all_logged(self):
        with patch.object(logging.Logger, 'warn', return_value=None) as log:
            sock = TestSocketWrapper.SocketMock()
            sock.send = Mock(return_value=MSG_SIZE - 1)
            wrapper = SocketWrapper(sock)
            wrapper.send('data')

            self.assertTrue(log.called)

    def test_property(self):
        sock = object()
        wrapper = SocketWrapper(sock)
        self.assertIs(sock, wrapper.socket)


class TestConfiguration(unittest.TestCase):
    def test_default_port(self):
        conf = Configuration('nonexistent_file.cfg')
        self.assertEqual(conf.default_server_port, conf.server_port)

    def test_default_ip(self):
        conf = Configuration('nonexistent_file.cfg')
        self.assertEqual(conf.default_server_ip, conf.server_ip)

    def test_log_missing_port(self):
        with patch.object(logging.Logger, 'warn', return_value=None) as log:
            conf = Configuration('nonexistent_file.cfg')
            conf.server_port
            self.assertTrue(log.called)

    def test_log_missing_ip(self):
        with patch.object(logging.Logger, 'warn', return_value=None) as log:
            conf = Configuration('nonexistent_file.cfg')
            conf.server_ip
            self.assertTrue(log.called)


class TestMessage(unittest.TestCase):
    def test_payload(self):
        obj = object()
        message = Message(obj)
        self.assertIs(obj, message.payload())

    def test_str(self):
        payload = 'some payload'
        message = Message(payload)
        self.assertIn(payload, str(message))


class TestGame(unittest.TestCase):
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

if __name__ == '__main__':
    unittest.main()
