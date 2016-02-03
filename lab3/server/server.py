import logging
import socket

from common.configuration import Configuration
from common.socket_wrapper import SocketWrapper

logger = logging.getLogger(__name__)


class Server:
    def __init__(self):
        self._config = Configuration()
        self._sock = None
        self._game = None

    def start(self):
        try:
            self._connect()
            while True:
                logger.debug('Awaiting an user')
                user = self._accept_user()
                g = user.receive().payload
                game = g(user)

                game.start()
                game.join()

        except KeyboardInterrupt:
            logger.info('Shutting down the server because of: Keyboard interruption')
        except ShutDownServer as e:
            logger.info('Shutting down the server because of: {}'.format(e))

    def stop(self):
        if self._sock is not None:
            self._sock.close()

    def _connect(self):
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
            raise ShutDownServer('Deploying the server has failed')

    def _accept_user(self):
        client_socket, address = self._sock.accept()
        logger.info('Client connected from {}'.format(address))
        return SocketWrapper(client_socket)


class ShutDownServer(Exception):
    pass
