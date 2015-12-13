import argparse
import logging

import sys

from client.client import Client
from server.server import Server

logging.basicConfig(filename='all.log', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(name)s %(message)s')

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Tic Tac Toe')
    subparsers = parser.add_subparsers(title='module', dest='module')
    subparsers.required = True
    subparsers.add_parser('server', help='start the server')
    subparsers.add_parser('client', help='start a client')

    args = parser.parse_args()

    if args.module == 'server':
        server = Server()
        try:
            server.start()
        except BaseException as e:
            logger.error('Process interrupted, stopping the server', exc_info=e)
        finally:
            server.stop()
    elif args.module == 'client':
        client = Client()
        try:
            client.connect()
            client.run()
        except BaseException as e:
            logger.error('Process interrupted, disconnecting the client', exc_info=e)
        finally:
            client.disconnect()
    else:
        print('unknown module {}'.format(args.module), file=sys.stderr)


if __name__ == '__main__':
    main()
