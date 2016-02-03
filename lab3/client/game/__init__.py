from abc import ABCMeta, abstractmethod

from common.socket_wrapper import SocketWrapper
from server.game import GameChooser


class ClientGame(metaclass=ABCMeta):
    def __init__(self, server: SocketWrapper):
        self._server = server
        server.send(GameChooser(self.server_game))

    @property
    @abstractmethod
    def server_game(self):
        pass

    @abstractmethod
    def run(self):
        pass
