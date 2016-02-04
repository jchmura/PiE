import logging
import unittest
from unittest.mock import patch, Mock

from common.configuration import Configuration
from common.message import Message
from common.socket_wrapper import SocketWrapper, MSG_SIZE


class TestConfiguration(unittest.TestCase):
    def test_default_port(self):
        conf = Configuration('nonexistent_file.cfg')
        self.assertEqual(conf.default_server_port, conf.server_port)

    def test_default_ip(self):
        conf = Configuration('nonexistent_file.cfg')
        self.assertEqual(conf.default_server_ip, conf.server_ip)

    def test_log_missing_port(self):
        with patch.object(logging.Logger, 'warn', return_value=None) as log:
            conf = Configuration('nonexistent_file.cfg')
            conf.server_port
            self.assertTrue(log.called)

    def test_log_missing_ip(self):
        with patch.object(logging.Logger, 'warn', return_value=None) as log:
            conf = Configuration('nonexistent_file.cfg')
            conf.server_ip
            self.assertTrue(log.called)


class TestSocketWrapper(unittest.TestCase):
    class SocketMock:
        def __init__(self):
            self.payload = None

        def send(self, data):
            self.payload = data
            return len(data)

        def recv(self, size):
            return self.payload

    def test_pass_through(self):
        sock = TestSocketWrapper.SocketMock()
        wrapper = SocketWrapper(sock)
        data = 'some data'
        wrapper.send(data)
        received = wrapper.receive()
        self.assertEqual(data, received)

    def test_message_size(self):
        sock = TestSocketWrapper.SocketMock()
        wrapper = SocketWrapper(sock)
        data = 'some data'
        wrapper.send(data)

        self.assertEqual(MSG_SIZE, len(sock.payload))

    def test_not_sent_all_logged(self):
        with patch.object(logging.Logger, 'warn', return_value=None) as log:
            sock = TestSocketWrapper.SocketMock()
            sock.send = Mock(return_value=MSG_SIZE - 1)
            wrapper = SocketWrapper(sock)
            wrapper.send('data')

            self.assertTrue(log.called)

    def test_property(self):
        sock = object()
        wrapper = SocketWrapper(sock)
        self.assertIs(sock, wrapper.socket)


class TestMessage(unittest.TestCase):
    def test_payload(self):
        obj = object()
        message = Message(obj)
        self.assertIs(obj, message.payload)

    def test_str(self):
        payload = 'some payload'
        message = Message(payload)
        self.assertIn(payload, str(message))
