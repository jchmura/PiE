import argparse
import logging
import re
import subprocess
import time
from os.path import abspath

from daemon import Daemon


def logger(name):
    def decorator(fun):
        def wrapper(*args, **kwargs):
            result = fun(*args, **kwargs)
            logging.getLogger(name).info('{:.2f}%'.format(result))
            return result

        return wrapper

    return decorator


class Monitor(Daemon):
    def __init__(self, pidfile):
        super().__init__(pidfile)
        self.cpu = False
        self.mem = False
        self.interval = 0
        self.file = ''

    def run(self):
        logging.basicConfig(format='%(asctime)s %(name)s %(message)s', filename=self.file, level=logging.DEBUG)
        while True:
            if self.cpu:
                self.get_cpu()
            if self.mem:
                self.get_mem()

            time.sleep(self.interval)

    @staticmethod
    @logger('CPU')
    def get_cpu():
        top = subprocess.getoutput('top -bn1')
        for line in top.split('\n'):
            if 'Cpu(s)' in line:
                match = re.search(r'.*, *([0-9.]*)%* id.*', line)
                if match:
                    idle = match.group(1)
                    return 100 - float(idle)

    @staticmethod
    @logger('MEM')
    def get_mem():
        with open('/proc/meminfo') as meminfo:
            available, total = 0, 0
            for line in meminfo:
                if 'MemTotal' in line:
                    total = int(line.split()[1])
                elif 'MemAvailable' in line:
                    available = int(line.split()[1])
            return available / total * 100


def main():
    parser = argparse.ArgumentParser(description='System monitor daemon')
    parser.add_argument('--pid', help='PID file of the daemon (default is %(default)s)', default='monitor.pid')

    subparsers = parser.add_subparsers(title='commands', dest='command')
    subparsers.required = True
    start_parser = subparsers.add_parser('start', help='start the daemon')
    start_parser.add_argument('--cpu', action='store_true', help='save the CPU usage')
    start_parser.add_argument('--mem', action='store_true', help='save the memory usage')
    start_parser.add_argument('--file', '-f', help='file where the information should be saved (default is %(default)s',
                              default='monitor.log')
    start_parser.add_argument('--interval', '-n',
                              help='How often (in sec) information should be collected (default is %(default)s)',
                              default=5, type=float)
    stop_parser = subparsers.add_parser('stop', help='stop the daemon')

    args = parser.parse_args()

    monitor = Monitor(abspath(args.pid))
    if args.command == 'stop':
        monitor.stop()
    elif args.command == 'start':
        monitor.cpu = args.cpu
        monitor.mem = args.mem
        monitor.interval = args.interval
        monitor.file = abspath(args.file)
        monitor.start()


if __name__ == '__main__':
    main()
