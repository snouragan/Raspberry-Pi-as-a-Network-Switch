# library to convert the bytes sent from arduino 
# to information about the relay state
# 0 - relay on 
# 1 - relay off
import sys
import curses
from curses import wrapper, textpad

class Relay:
    state = 0b11111111
    numberOfRelays = 6 
    stdscr = curses.initscr()
    SCREEN_WIDTH = curses.COLS
    SCREEN_HEIGHT = curses.LINES
    WIDTH = SCREEN_WIDTH//10
    HEIGHT = SCREEN_HEIGHT//3
    SPACE = (SCREEN_WIDTH - (WIDTH*numberOfRelays)) // (numberOfRelays+1)
    MARGINX = (SCREEN_WIDTH - (numberOfRelays*WIDTH + (numberOfRelays+1)*SPACE)) // 2
    MARGINY = 1

    def __init__(self, number, name="Relay"):
        self.name = name
        self.number = number
        curses.noecho()
        curses.cbreak()
        Relay.stdscr.keypad(True)
    def getNumber(self):
        return self.number
    def isOn(self):
        return False if self.state & 1<<self.getNumber() else True 
    def drawRelay(self):
        uly = Relay.MARGINY
        ulx = Relay.MARGINX + Relay.SPACE*(self.number+1) + self.number*Relay.WIDTH 
        lry = Relay.MARGINY + Relay.HEIGHT
        lrx = ulx + Relay.WIDTH
        curses.textpad.rectangle(Relay.stdscr, uly, ulx, lry, lrx)
        Relay.stdscr.refresh()
    def drawDetails(self):
        pass
    def debug(self):
        print("WIDTH:", Relay.WIDTH, "HEIGHT:", Relay.HEIGHT, "SPACE:", Relay.SPACE, "MARGINX:", Relay.MARGINX, "uly:", Relay.MARGINY, "ulx:", Relay.MARGINX + Relay.SPACE*(self.number+1) + self.number*Relay.WIDTH, "lry:",Relay.MARGINY + Relay.HEIGHT, "lrx:", Relay.MARGINX + Relay.SPACE*(self.number+1) + self.number*Relay.WIDTH + Relay.WIDTH)
 

if __name__ == '__main__':
    try:
        numberOfRelays = 6
        relay = []
        for _ in range(numberOfRelays):
            relay.append(Relay(_))
            relay[_].debug()
#        print '{}'.format(Relay.stdscr.getmaxyx())
#        for _ in range(numberOfRelays):
#                relay[_].drawRelay()
        while True:
            for _ in range(numberOfRelays):
                relay[_].drawRelay()
            pass
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


