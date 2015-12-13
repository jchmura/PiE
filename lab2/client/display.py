import curses
import logging

from common.game import Sign

logger = logging.getLogger(__name__)


def wait(fun):
    def wrapped(*args, **kwargs):
        self = args[0]
        value = fun(*args, **kwargs)
        self.stdscr.getch()
        return value

    return wrapped


class Display:
    title_y = 0
    title_x = 5

    message_y = 2
    message_x = 5

    grid_y = 6
    grid_x = 10

    def __init__(self, sign, board, client=None):
        self.sign = sign
        self.board = board
        self.client = client
        self.stdscr = curses.initscr()
        curses.noecho()  # don't display keys automatically
        curses.cbreak()  # no enter required
        self.stdscr.keypad(True)  # handle special characters
        self.stdscr.leaveok(False)

        self._title = ''
        self._message = ''

    def exit(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def quit(self):
        self.display_title('Press q to exit')
        while True:
            ch = self.stdscr.getch()
            if ch == ord('q'):
                self.exit()
                break

    def display_title(self, title):
        self._title = title
        self._display_text(self.title_y, self.title_x, title)

    def display_message(self, message):
        self.clear_message()
        self._message = message
        self._display_text(self.message_y, self.message_x, message)

    def clear_message(self):
        self._display_text(self.message_y, self.message_x, ' ' * len(self._message))

    def _display_text(self, y, x, text):
        orig_y, orig_x = self.stdscr.getyx()
        self.stdscr.addstr(y, x, text)
        self.stdscr.move(orig_y, orig_x)
        self._refresh()

    def clear(self):
        self.stdscr.erase()

    def display_empty_grid(self):
        for y in range(self.grid_y, self.grid_y + 5, 2):
            for x in range(self.grid_x + 1, self.grid_x + 4, 2):
                self.stdscr.addch(y, x, curses.ACS_VLINE)

        for y in range(self.grid_y + 1, self.grid_y + 4, 2):
            for x in range(self.grid_x, self.grid_x + 5):
                self.stdscr.addch(y, x, curses.ACS_HLINE)
        curses.curs_set(0)

    def fill_grid(self):
        board_values = self.board.board
        for x in range(3):
            for y in range(3):
                value = board_values[x][y]
                if value != Sign.empty:
                    self.stdscr.addch(self._y_to_curses(y), self._x_to_curses(x), str(value))
        self._refresh()

    def _refresh(self):
        self.stdscr.refresh()

    def input(self):
        curses.curs_set(2)
        x, y = 1, 1
        self.stdscr.move(self._y_to_curses(y), self._x_to_curses(x))
        self._refresh()
        while True:
            ch = self.stdscr.getch()
            if ch in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
                self._move(ch)
            elif ch in [curses.KEY_ENTER, ord('\n')]:
                if self._put():
                    break
            else:
                logger.warn('Unknown key {}'.format(ch))

    def _move(self, ch):
        x, y = self._xy_from_curses()
        if ch == curses.KEY_LEFT and x > 0:
            x -= 1
        elif ch == curses.KEY_RIGHT and x < 2:
            x += 1
        elif ch == curses.KEY_UP and y > 0:
            y -= 1
        elif ch == curses.KEY_DOWN and y < 2:
            y += 1
        self.stdscr.move(self._y_to_curses(y), self._x_to_curses(x))
        self._refresh()

    def _put(self):
        x, y = self._xy_from_curses()
        if self.board.board[x][y] == Sign.empty:
            self.board.put(x, y, self.sign)
            curses.curs_set(0)
            self.fill_grid()
            return True
        return False

    def _y_to_curses(self, y):
        return int(self.grid_y + y * 2)

    def _x_to_curses(self, x):
        return int(self.grid_x + x * 2)

    def _xy_from_curses(self):
        y, x = self.stdscr.getyx()
        return (x - self.grid_x) // 2, (y - self.grid_y) // 2
