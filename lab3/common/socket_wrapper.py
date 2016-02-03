import logging
import pickle
import socket

from common.message import Message

MSG_SIZE = 2048
logger = logging.getLogger(__name__)


class SocketWrapper:
    def __init__(self, sock: socket.socket):
        self._sock = sock

    @property
    def socket(self):
        return self._sock

    def send(self, message: Message):
        pickled = pickle.dumps(message)
        message_length = len(pickled)

        if message_length < MSG_SIZE:
            pickled += b' ' * (MSG_SIZE - message_length)
        elif message_length > MSG_SIZE:
            logger.warn('Message length is longer than the allowed message size')

        sent = self._sock.send(pickled)
        if sent != MSG_SIZE:
            logger.warn('Sent only {} bytes instead of {}'.format(sent, MSG_SIZE))

    def receive(self) -> Message:
        pickled = self._sock.recv(MSG_SIZE)
        return pickle.loads(pickled)
