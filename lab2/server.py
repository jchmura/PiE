import logging
import socket
import time
from threading import Thread

import configuration
import message
from game import Board, Sign
from socket_wrapper import SocketWrapper

logger = logging.getLogger(__name__)


class Server:
    def __init__(self):
        self._config = configuration.Configuration()
        self._sock = None
        self._player1 = None
        self._player2 = None
        self._board = Board()
        self._new_board = False
        self.round_sign = Sign.x

    @property
    def full(self):
        return self._player1 is not None and self._player2 is not None

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._new_board = True
        self._board.board = value

    def start(self):
        ip = self._config.server_ip
        port = self._config.server_port
        logger.debug('Starting server at {}:{}'.format(ip, port))
        try:
            self._sock = socket.socket()
            self._sock.bind((ip, port))
            self._sock.listen()
            logger.info('Listening on {}:{}'.format(ip, port))
        except Exception as e:
            logger.error('Could not start server', exc_info=e)
            return

        while self._player2 is None:
            client_socket, address = self._sock.accept()
            logger.info('Client connected from {}'.format(address))
            if self._player1 is None:
                self._player1 = ClientConnection(Sign.x, client_socket, self)
                self._player1.start()
            else:
                self._player2 = ClientConnection(Sign.o, client_socket, self)
                self._player2.start()

        logger.info('Both players are connected, the game has started')
        self._player1.send_board(self._board.board)
        self._player2.send_board(self._board.board)

        while not self._board.finished:
            if self._new_board:
                self._new_board = False
                new_board = self._board.board
                self.round_sign = Sign.o if self.round_sign == Sign.x else Sign.x

                logger.info("Received a new board, it is {}'s round now".format(self.round_sign))
                logger.debug('Sending new board to both players\n{}'.format(self._board))
                self._player1.send_board(new_board)
                self._player2.send_board(new_board)
            time.sleep(.1)

        logger.info('The game have finished, informing both players')
        self._player1.finish()
        self._player2.finish()
        logger.info('Players have been informed')

        self._player1.join()
        self._player2.join()

    def stop(self):
        if self._sock is not None:
            self._sock.close()
            self._sock = None
        else:
            logger.debug('Socket is not open, no need to close it')


class ClientConnection(Thread):
    def __init__(self, sign, sock, server):
        super().__init__(name='client {}'.format(sign))
        self._sign = sign
        self._sock = SocketWrapper(sock)
        self._server = server
        self._finished = False
        self._board_to_send = None
        self._logger = logging.getLogger(__name__ + str(sign))

    def finish(self):
        self._finished = True

    def send_board(self, board):
        self._board_to_send = board

    def _wait_for_board(self):
        while self._board_to_send is None:
            if self._finished:
                raise GameFinished
            time.sleep(.1)
        board = self._board_to_send
        self._board_to_send = None
        return board

    def run(self):
        self._sock.send(message.SignMessage(self._sign))
        self._sock.send(message.ReadyMessage(self._server.full))
        while not self._server.full:
            time.sleep(.1)
        self._sock.send(message.ReadyMessage(True))
        self._logger.debug('The game is ready, player have been informed')

        self._logger.info('Waiting for the first board')
        board = self._wait_for_board()
        self._logger.debug('Sending the first board to the player')
        self._sock.send(message.BoardMessage(board))

        try:
            while True:
                self._round()
        except GameFinished:
            self._logger.info('The game have finished, sending last board')
            self._sock.send(message.BoardMessage(self._server.board.board))
            self._logger.info('Sending end message')
            self._sock.send(message.EndMessage(self._server.board.tie()))
            self._sock.socket.close()

    def _round(self):
        round_sign = self._server.round_sign
        self._sock.send(message.RoundMessage(round_sign))
        if round_sign == self._sign:
            self._logger.debug("It is my player's round, waiting for the new board")
            board = self._sock.receive().payload()
            self._logger.debug('Board received')
            self._server.board = board

        self._logger.info('Waiting for the board for this round')
        board = self._wait_for_board()
        self._logger.debug('Sending the new board to the player')
        self._sock.send(message.BoardMessage(board))


class GameFinished(Exception):
    pass