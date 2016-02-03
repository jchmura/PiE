import copy
import logging
import random
from enum import Enum

from common.message import Message
from common.socket_wrapper import SocketWrapper
from server.game import ServerGame

logger = logging.getLogger(__name__)


class Sign(Enum):
    empty = ' '
    x = 'X'
    o = 'O'

    def __str__(self):
        return self.value


class TicTacToe(ServerGame):
    user_sign = Sign.x
    computer_sign = Sign.o

    def __init__(self, user: SocketWrapper):
        super().__init__(user)
        self._board = Board()

    def run(self):
        logger.info('Starting the game Tic Tac Toe')
        while True:
            user_move = self._user.receive()
            self._board.board = user_move.payload
            if self._board.finished:
                self._send_finish()
                break
            else:
                self._make_move()
                self._user.send(Move(self._board.board))

        logger.info('The game Tic Tac Toe is finished')

    def _send_finish(self):
        if self._board.won(self.user_sign):
            result = Finish.Result.win
        elif self._board.won(self.computer_sign):
            result = Finish.Result.lost
        else:
            result = Finish.Result.tie

        self._user.send(Finish(result))

    def _make_move(self):
        board = self._board.board
        empty = []

        for x in range(3):
            for y in range(3):
                if board[x][y] == Sign.empty:
                    empty.append((x, y))

        x, y = random.choice(empty)
        self._board.put(x, y, self.computer_sign)


class Board:
    def __init__(self):
        self._board = [[Sign.empty] * 3 for i in range(3)]

    @property
    def board(self):
        return copy.deepcopy(self._board)

    @board.setter
    def board(self, value):
        if len(value) != 3:
            raise ValueError('Board must be of shape 3x3')
        for row in value:
            if len(row) != 3:
                raise ValueError('Board must be of shape 3x3')
            for sign in row:
                if not isinstance(sign, Sign):
                    raise ValueError('Unsupported sign {}'.format(sign))

        self._board = copy.deepcopy(value)

    @property
    def finished(self):
        return self.won(Sign.x) or self.won(Sign.o) or self.tie()

    def won(self, sign):
        for x in range(3):
            if self._board[x][0] == sign and self._board[x][1] == sign and self._board[x][2] == sign:
                return True

        for y in range(3):
            if self._board[0][y] == sign and self._board[1][y] == sign and self._board[2][y] == sign:
                return True

        if self._board[0][0] == sign and self._board[1][1] == sign and self._board[2][2] == sign:
            return True

        return False

    def tie(self):
        for x in range(3):
            for y in range(3):
                if self._board[x][y] == Sign.empty:
                    return False
        return True

    def put(self, x, y, sign):
        if sign not in [Sign.x, Sign.o]:
            raise ValueError('Unsupported sign {}'.format(sign))
        if x > 2 or y > 2:
            raise IndexError('({}; {}) is outside the board'.format(x, y))
        if self._board[x][y] != Sign.empty:
            raise IndexError('({}; {}) already has a value'.format(x, y))

        self._board[x][y] = sign

    def __str__(self):
        ret = ''
        for y in range(3):
            for x in range(3):
                sign = self._board[x][y]
                ret += str(sign)
                if x < 2:
                    ret += '|'
            if y < 2:
                ret += '\n'
        return ret


class Move(Message):
    pass


class Finish(Message):
    class Result(Enum):
        win = 1
        lost = 2
        tie = 3
