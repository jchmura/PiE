import logging
import random
from enum import Enum

from common.message import Message
from . import ServerGame

logger = logging.getLogger(__name__)


class MoreOrLess(ServerGame):
    min_value = 10
    max_value = 100

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = random.randint(self.min_value, self.max_value)
        logger.info('The value is {}'.format(self._value))

    def run(self):
        logger.info('Starting the game More or Less')
        while True:
            self._user.send(EnterNumber())
            number = self._user.receive().payload
            logger.debug('Received number {}'.format(number))

            if number > self._value:
                direction = Result.Direction.more
            elif number < self._value:
                direction = Result.Direction.less
            else:
                direction = Result.Direction.equal

            logger.debug('Sending direction {}'.format(direction))
            self._user.send(Result(direction))

            if direction is Result.Direction.equal:
                break

        logger.info('The game More or Less is finished')


class EnterNumber(Message):
    pass


class EnteredNumber(Message):
    pass


class Result(Message):
    class Direction(Enum):
        more = 1
        less = -1
        equal = 0
