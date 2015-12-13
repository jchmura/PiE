class Message:
    def __init__(self, payload=None):
        self._payload = payload

    def payload(self):
        return self._payload

    def __str__(self):
        return '{} {}'.format(type(self).__name__, self.payload())


class SignMessage(Message):
    pass


class ReadyMessage(Message):
    pass


class RoundMessage(Message):
    pass


class BoardMessage(Message):
    pass


class EndMessage(Message):
    pass
