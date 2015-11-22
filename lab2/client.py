import logging
import socket

import configuration
from display import Display
from game import Board
from message import RoundMessage, EndMessage, BoardMessage
from socket_wrapper import SocketWrapper


class Client:
    def __init__(self):
        self._config = configuration.Configuration()
        self._sock = None
        self._board = Board()
        self._display = None
        self._logger = logging.getLogger(__name__)

    def connect(self):
        self._sock = SocketWrapper(socket.socket())
        self._sock.socket.connect((self._config.server_ip, self._config.server_port))

    def run(self):
        sign = self.receive().payload()
        self._display = Display(sign, self._board, self)
        self._display.display_empty_grid()
        self._display.display_title('You are {}'.format(sign))
        self._logger = logging.getLogger(__name__ + str(sign))
        self._logger.debug('Connected to server')

        ready = self.receive().payload()
        if not ready:
            self._display.display_message('Waiting for opponent...')
            self._logger.debug('Waiting for opponent')

        ready = self.receive().payload()
        if not ready:
            self._logger.warn('Now the server should be ready, something bad happened')
            return
        self._display.clear_message()
        self._logger.info('Everyone is connected, the game can start')

        while True:
            message = self.receive()
            if isinstance(message, BoardMessage):
                board = message.payload()
                self._logger.debug('Received new board')
                self._board.board = board
                self._display.fill_grid()
                self._logger.debug('New board displayed on the screen')
            elif isinstance(message, RoundMessage):
                round = message.payload()
                if round == sign:
                    self._logger.debug('It is my round')
                    self._display.display_message('This is your round')
                    self._display.input()
                    self._logger.info('Move is made, sending new board to the server\n{}'.format(self._board))
                    self.send(BoardMessage(self._board.board))
                else:
                    self._logger.debug("It is my opponent's round")
                    self._display.display_message("This is your opponent's round")
            elif isinstance(message, EndMessage):
                self._logger.info('The game has ended')
                tie = message.payload()
                if tie:
                    self._display.display_message("Is's a tie")
                    self._logger.debug("It's a tie")
                else:
                    winner = self._board.won(sign)
                    if winner:
                        self._display.display_message('You won!')
                    else:
                        self._display.display_message('You lost')
                    self._logger.debug('Have I won? {}'.format(winner))
                self._display.quit()
                break
            else:
                self._logger.warn('Unknown message: {}'.format(message))

    def receive(self):
        return self._sock.receive()

    def send(self, message):
        self._sock.send(message)

    def disconnect(self):
        if self._sock is not None:
            self._sock.socket.close()
            self._sock = None
            self._logger.info('Socket closed')
        else:
            self._logger.debug('Socket is not open, no need to close it')

        if self._display is not None:
            self._display.exit()
