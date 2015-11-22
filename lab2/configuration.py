import configparser
import logging

logger = logging.getLogger(__name__)


class Configuration:
    default_server_ip = 'localhost'
    default_server_port = 8000

    def __init__(self, filename='config.cfg'):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

    @property
    def server_ip(self):
        try:
            return self.config.get('server', 'ip')
        except KeyError:
            logging.warning(
                    'No IP specified for the server in the configuration, using {}'.format(self.default_server_ip))
            return self.default_server_ip

    @property
    def server_port(self):
        try:
            return self.config.getint('server', 'port')
        except KeyError:
            logging.warning(
                    'No port specified for the server in the configuration, using {}'.format(self.default_server_port))
            return self.default_server_port
