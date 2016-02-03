import logging

from client.game import ClientGame
from server.game.more_less import EnterNumber, EnteredNumber, Result
from server.game.more_less import MoreOrLess as ServerMoreOrLess

logger = logging.getLogger(__name__)


class MoreOrLess(ClientGame):

    @property
    def server_game(self):
        return ServerMoreOrLess

    def run(self):
        while True:
            rcv = self._server.receive()
            if isinstance(rcv, EnterNumber):
                number = self._get_number()
                self._server.send(EnteredNumber(number))
            if isinstance(rcv, Result):
                if not self._should_continue(rcv.payload):
                    break

    @staticmethod
    def _get_number():
        while True:
            number = input('Enter a number: ')
            if number.isdigit():
                return int(number)

    @staticmethod
    def _should_continue(direction):
        if direction is not Result.Direction.equal:
            print('The number you entered is {} than the result'.format(direction.name))
            return True
        else:
            print('You guessed the result, bravo!')
            return False
