import logging
import socket
from enum import Enum

from client.game import ClientGame
from common.configuration import Configuration
from common.socket_wrapper import SocketWrapper

logger = logging.getLogger(__name__)


class AvailableGame(Enum):
    pass


class Client:
    def __init__(self):
        self._config = Configuration()
        self._sock = None

    def connect(self):
        self._sock = SocketWrapper(socket.socket())
        self._sock.socket.connect((self._config.server_ip, self._config.server_port))

    def disconnect(self):
        if self._sock is not None:
            self._sock.socket.close()
            self._sock = None
            logger.info('Socket closed')
        else:
            logger.debug('Socket is not open, no need to close it')

    def run(self):
        game = self._choose_game()
        game.run()

    def _choose_game(self) -> ClientGame:
        print('Choose the game you want:')
        games = list(AvailableGame)
        for i, game in enumerate(games, start=1):
            print('{}. {}'.format(i, game.name))

        choice = None
        while True:
            choice = input('Choice ({}-{}): '.format(1, len(games)))
            if choice.isdigit():
                break

        choice = int(choice)
        game = games[choice - 1]
        return game.value(self._sock)


