import copy
from enum import Enum


class Sign(Enum):
    empty = ' '
    x = 'X'
    o = 'O'

    def __str__(self):
        return self.value


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
