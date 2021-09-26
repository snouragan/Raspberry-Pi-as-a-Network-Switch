# library to convert the bytes sent from arduino 
# to information about the relay state
# 0 - relay on 
# 1 - relay off

from graphics import *
import curses
from curses import wrapper

class Relay:
    state = 0b11111111
    SCREEN_WIDTH = curses.COLS
    SCREEN_HEIGTH = curses.LINES
    def __init__(self, number):
        self.number = number
    def getNumber(self):
        return self.number
    def isOn(self):
        return False if self.state & 1<<self.getNumber() else True 

def TEST_1():
    relay = Relay(0)
    print(relay.getNumber())

def TEST_2():
    relays = []
    for _ in range(8):
        relays.append( Relay(_))
    for relay in relays:
        print(relay.getNumber(), sep=' ', end = '\n')
def TEST_3():
    relays = []
    for _ in range(8):
        relays.append( Relay(_))
    Relay.state = 0b00100100
    for relay in relays:
        print (relay.isOn(), sep =' ', end = '\n')

def main(stdscr):
    stdscr.clear()

    for _ in range(0, 11):
        v = _ - 10
        stdscr.addstr(_, 0, '10 divided by {} is {}'.format(v, 10/v))

        stdscr.refresh()
        stdscr.getkey()

if __name__ == '__main__':
    #TEST_1()
    #TEST_2()    
    #TEST_3()
    stdscr = curses.initscr()
    wrapper(main(stdscr))    
