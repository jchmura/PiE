class Message:
    def __init__(self, payload=None):
        self._payload = payload

    @property
    def payload(self):
        return self._payload

    def __str__(self):
        return '{} {}'.format(type(self).__name__, self.payload())