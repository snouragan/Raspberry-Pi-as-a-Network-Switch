# library to convert the bytes sent from arduino 
# to information about the relay state
# 0 - relay on 
# 1 - relay off
import sys
import curses
from curses import wrapper, textpad

# move cursor: window.move(new y, new x)
# get str from user: window.getstr(y,x,n) 
# get key: window.getke([y,x])



class Relay:
        state = 0b11111111
        numberOfRelays = 8 
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
                curses.start_color()
                self.background()
        def __del__(self):
                curses.nocbreak()
                Relay.stdscr.keypad(False) 
                curses.echo()
                curses.endwin()
        def isOn(self):
                return False if self.state & 1<< self.number else True 
        def drawRelay(self):
                self.uly = Relay.MARGINY
                self.ulx = Relay.MARGINX + Relay.SPACE*(self.number+1) + self.number*Relay.WIDTH 
                self.lry = Relay.MARGINY + Relay.HEIGHT
                self.lrx = self.ulx + Relay.WIDTH
                curses.textpad.rectangle(Relay.stdscr, self.uly, self.ulx, self.lry, self.lrx)
                Relay.stdscr.refresh()
        def drawName(self):
                length = len(self.name)
                self.NAMEX = self.ulx + ((self.lrx - self.ulx) // 2) - (length//2)
                self.NAMEY = (Relay.HEIGHT // 4) + Relay.MARGINY
                Relay.stdscr.addstr(self.NAMEY, self.NAMEX, self.name)
        def drawNumber(self):
                self.NUMBERX = self.ulx + ((self.lrx - self.ulx) // 2)
                self.NUMBERY = (Relay.HEIGHT // 2) + Relay.MARGINY
                Relay.stdscr.addstr(self.NUMBERY, self.NUMBERX, str(self.number))
        def drawDetails(self):
                self.drawName()
                self.drawNumber()
        def drawState(self):
                self.STATEY = Relay.HEIGHT*2 + Relay.MARGINY
                if self.isOn():
                        self.STATEX = self.ulx + ((self.lrx - self.ulx) // 2) - (len('ON')//2)
                        state = 'ON'
                else:
                        self.STATEX = self.ulx + ((self.lrx - self.ulx) // 2) - (len('OFF')//2)
                        state = 'OFF'
                curses.textpad.rectangle(Relay.stdscr, self.STATEY-1, self.STATEX-1, self.STATEY+1, self.STATEX+3)
                Relay.stdscr.addstr(self.STATEY, self.STATEX, state)
        def drawCommands(self):
                key = 'F' + str(self.number+1)
                Relay.stdscr.addstr(Relay.HEIGHT*2 + Relay.MARGINY + 3, self.ulx + ((self.lrx - self.ulx) // 2), key)
                Relay.stdscr.addstr(Relay.SCREEN_HEIGHT-1, 1, 'Toggle state on key press')
        def drawByteState(self):
                self.STATEX = (Relay.SCREEN_WIDTH//2) - 6
                self.STATEY = Relay.SCREEN_HEIGHT//2
                Relay.stdscr.addstr(self.STATEY-1, self.STATEX+4, 'BYTE')
                Relay.stdscr.addstr(self.STATEY, self.STATEX, str(bin(Relay.state)))
                Relay.stdscr.addstr(self.STATEY, self.STATEX, '  ')
        def background(self):
                self.drawRelay()
                self.drawDetails()
                self.drawState()
                self.drawCommands()
                self.drawByteState()
                Relay.stdscr.refresh()
        def readKey():
                key = Relay.stdscr.get_wch()
                return{
                        KEY_F1 : 1,
                        KEY_F2 : 2,
                        KEY_F3 : 3,
                        KEY_F4 : 4,
                        KEY_F5 : 5,
                        KEY_F6 : 6,
                        KEY_F7 : 7,
                        KEY_F8 : 8,
                       }[key]
        def toggleRelay():
                relayNumber = Relay.readKey()-1
                if Relay.state&relayNumber == 0:
                        Relay.state += 0b00000001 << relayNumber
                else:
                        Relay.state -= 0b00000001 >> relayNumber
        def debug(self):
                pass

if __name__ == '__main__':
        try:
                numberOfRelays = 8
                relay = []
                for _ in range(numberOfRelays):
                        relay.append(Relay(_))
                        relay[_].background()
                while True:
                        Relay.toggleRelay()
                        
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


