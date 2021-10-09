import curses
from curses import textpad
import sys


class Relay:
    state = 0b11111111
    number_of_relays = 8
    stdscr = curses.initscr()
    SCREEN_WIDTH = curses.COLS
    SCREEN_HEIGHT = curses.LINES
    WIDTH = SCREEN_WIDTH // 10
    HEIGHT = SCREEN_HEIGHT // 3
    SPACE = (SCREEN_WIDTH - (WIDTH * number_of_relays)) // (number_of_relays + 1)
    MARGINX = (SCREEN_WIDTH - (number_of_relays * WIDTH + (number_of_relays + 1) * SPACE)) // 2
    MARGINY = 1

    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)  # ON
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)  # OFF
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_CYAN)  # RELAY_FILL
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_CYAN)  # RELAY_WRITING
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_WHITE)  # BORDER

    curses.curs_set(0)  # cursor set to invisible

    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.start_color()

    def __init__(self, number, name="Relay"):
        self.name = name
        self.number = number
        self.uly = None
        self.ulx = None
        self.lry = None
        self.lrx = None
        self.NAMEX = None
        self.NAMEY = None
        self.NUMBERX = None
        self.NUMBERY = None
        self.STATEY = None
        self.STATEX = None
        self.BYTESTATEX = None
        self.BYTESTATEY = None

    def __del__(self):
        curses.nocbreak()
        Relay.stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    def is_on(self):
        return False if Relay.state & 1 << self.number else True

    def draw_relay(self):
        self.uly = Relay.MARGINY
        self.ulx = Relay.MARGINX + Relay.SPACE * (self.number + 1) + self.number * Relay.WIDTH
        self.lry = Relay.MARGINY + Relay.HEIGHT
        self.lrx = self.ulx + Relay.WIDTH

        Relay.stdscr.attron(curses.color_pair(5))
        curses.textpad.rectangle(Relay.stdscr, self.uly, self.ulx, self.lry, self.lrx)
        Relay.stdscr.attron(curses.color_pair(5))

        Relay.stdscr.attron(curses.color_pair(3))
        for col in range(self.ulx + 1, self.lrx):
            for line in range(self.uly + 1, self.lry):
                Relay.stdscr.addch(line, col, ' ')
        Relay.stdscr.attroff(curses.color_pair(3))

    def draw_name(self):
        length = len(self.name)
        self.NAMEX = self.ulx + ((self.lrx - self.ulx) // 2) - (length // 2)
        self.NAMEY = (Relay.HEIGHT // 4) + Relay.MARGINY

        Relay.stdscr.attron(curses.color_pair(4))
        Relay.stdscr.addstr(self.NAMEY, self.NAMEX, self.name)
        Relay.stdscr.attroff(curses.color_pair(4))

    def draw_number(self):
        self.NUMBERX = self.ulx + ((self.lrx - self.ulx) // 2)
        self.NUMBERY = (Relay.HEIGHT // 2) + Relay.MARGINY

        Relay.stdscr.attron(curses.color_pair(4))
        Relay.stdscr.addstr(self.NUMBERY, self.NUMBERX, str(self.number + 1))
        Relay.stdscr.attroff(curses.color_pair(4))

    def draw_state(self):
        self.STATEY = Relay.HEIGHT * 2 + Relay.MARGINY
        if self.is_on():
            state = 'ON '
            self.STATEX = self.ulx + ((self.lrx - self.ulx) // 2) - (len(state) // 2)
            Relay.stdscr.attron(curses.color_pair(1))
            Relay.stdscr.addstr(self.STATEY, self.STATEX, state)
            Relay.stdscr.attroff(curses.color_pair(1))
        else:
            state = 'OFF'
            self.STATEX = self.ulx + ((self.lrx - self.ulx) // 2) - (len(state) // 2)
            Relay.stdscr.attron(curses.color_pair(2))
            Relay.stdscr.addstr(self.STATEY, self.STATEX, state)
            Relay.stdscr.attroff(curses.color_pair(2))

        Relay.stdscr.attron(curses.color_pair(5))
        curses.textpad.rectangle(Relay.stdscr, self.STATEY - 1, self.STATEX - 1, self.STATEY + 1, self.STATEX + 3)
        Relay.stdscr.attroff(curses.color_pair(5))

    def draw_commands(self):
        key = 'F' + str(self.number + 1)
        Relay.stdscr.addstr(Relay.HEIGHT * 2 + Relay.MARGINY + 3, self.ulx + ((self.lrx - self.ulx) // 2), key)
        Relay.stdscr.addstr(Relay.SCREEN_HEIGHT - 1, 1, 'Toggle state on key press')

    def draw_byte_state(self):
        self.BYTESTATEX = (Relay.SCREEN_WIDTH // 2) - 6
        self.BYTESTATEY = Relay.SCREEN_HEIGHT // 2

        Relay.stdscr.addstr(self.STATEY - 1, self.STATEX + 4, 'BYTE')
        Relay.stdscr.addstr(self.STATEY, self.STATEX, str(bin(Relay.state)))
        Relay.stdscr.addstr(self.STATEY, self.STATEX, '  ')

    @classmethod
    def update_screen(cls):
        if curses.is_term_resized(Relay.SCREEN_HEIGHT, Relay.SCREEN_WIDTH):
            new_dimensions = Relay.stdscr.getmaxyx()
            Relay.SCREEN_WIDTH = new_dimensions[1]
            Relay.SCREEN_HEIGHT = new_dimensions[0]
            Relay.WIDTH = Relay.SCREEN_WIDTH // 10
            Relay.HEIGHT = Relay.SCREEN_HEIGHT // 3
            Relay.SPACE = (Relay.SCREEN_WIDTH - (Relay.WIDTH * Relay.number_of_relays)) // (Relay.number_of_relays + 1)
            Relay.MARGINX = (Relay.SCREEN_WIDTH - (
                    Relay.number_of_relays * Relay.WIDTH + (Relay.number_of_relays + 1) * Relay.SPACE)) // 2
            Relay.MARGINY = 1
            Relay.stdscr.clear()
            Relay.stdscr.refresh()
            return True
        return False

    def background(self):
        self.draw_relay()
        self.draw_commands()
        self.draw_byte_state()
        self.draw_state()
        self.draw_name()
        self.draw_number()
        Relay.stdscr.refresh()


if __name__ == '__main__':
    try:
        number_of_relays = 8
        relays = []
        for _ in range(1, 1 + number_of_relays):
            relay = Relay(_)
        Relay.number_of_relays = number_of_relays
        for relay in relays:
            relay.background()

        while True:
            if Relay.update_screen():
                for relay in relays:
                    relay.background()

    except KeyboardInterrupt:
        curses.nocbreak()
        Relay.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        print('\nInterrupted')
        sys.exit(0)
    finally:
        curses.nocbreak()
        Relay.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
