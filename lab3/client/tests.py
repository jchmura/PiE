import socket
import unittest

from client.game.more_less import MoreOrLess
from client.game.tic_tac_toe import TicTacToe
from common.socket_wrapper import SocketWrapper


class SocketMock(socket.socket):
    def __init__(self):
        super().__init__()
        self.payload = None

    def send(self, data, **kwargs):
        self.payload = data
        return len(data)

    def recv(self, size, **kwargs):
        return self.payload


class ClientTest(unittest.TestCase):
    def test_more_or_less_server_game_sent(self):
        sock = SocketWrapper(SocketMock())
        more_less = MoreOrLess(sock)
        self.assertEqual(more_less.server_game, sock.receive().payload)

    def test_tic_tac_toe_server_game_sent(self):
        sock = SocketWrapper(SocketMock())
        tic_tac_toe = TicTacToe(sock)
        self.assertEqual(tic_tac_toe.server_game, sock.receive().payload)