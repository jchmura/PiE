import logging
import pickle

MSG_SIZE = 1024
logger = logging.getLogger(__name__)


class SocketWrapper:
    def __init__(self, sock):
        self._sock = sock

    @property
    def socket(self):
        return self._sock

    def send(self, message):
        pickled = pickle.dumps(message)
        message_length = len(pickled)
        if message_length < MSG_SIZE:
            pickled += b' ' * (MSG_SIZE - message_length)
        sent = self._sock.send(pickled)
        if sent != MSG_SIZE:
            logger.warn('Sent only {} bytes instead of {}'.format(sent, MSG_SIZE))

    def receive(self):
        pickled = self._sock.recv(MSG_SIZE)
        return pickle.loads(pickled)
