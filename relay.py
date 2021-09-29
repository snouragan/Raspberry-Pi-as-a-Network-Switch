# library to convert the bytes sent from arduino 
# to information about the relay state
# 0 - relay on 
# 1 - relay off
import sys
import curses
from curses import wrapper, textpad

class Relay:
    state = 0b11111111
    numberOfRelays = 8 
    stdscr = curses.initscr()
    SCREEN_WIDTH = curses.COLS
    SCREEN_HEIGHT = curses.LINES
    WIDTH = 8
    HEIGHT = 8
    SPACE = 0
    STARTY = 1
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
    def printParameters(self):
        Relay.stdscr.clear()
        Relay.stdscr.addstr(0, 0, str(Relay.SCREEN_WIDTH))
        Relay.stdscr.addstr(1, 0, str(Relay.SCREEN_HEIGHT))
    def setSpace():
        Relay.SPACE = (Relay.SCREEN_WIDTH - (Relay.WIDTH*Relay.numberOfRelays)) // (Relay.numberOfRelays+1)
    def drawRelay(self):
        Relay.setSpace()
        uly = Relay.STARTY
        ulx = Relay.SPACE*(self.number+1) + self.number*Relay.WIDTH 
        lry = Relay.STARTY + Relay.HEIGHT
        lrx = ulx + Relay.WIDTH
        curses.textpad.rectangle(Relay.stdscr, uly, ulx, lry, lrx)
        Relay.stdscr.refresh()
    def drawDetails(self):
        pass
if __name__ == '__main__':
    try:
        numberOfRelays = 8
        relay = []
        for _ in range(numberOfRelays):
            relay.append(Relay(_))
#        for _ in range(1, numberOfRelays+1):
#            Relay.numberOfRelays = _
#            print(Relay.numberOfRelays)
#            Relay.setSpace()
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
